#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys, traceback, csv
import configdb
from consolemsg import step, success, warn, error
from yamlns import namespace as ns
from erppeek import Client
from datetime import datetime

class ImportData:
    def read_employees_data_csv(self, csv_file):
        with open(csv_file, 'rb') as f:
            reader = csv.reader(f, delimiter=';')
            header = reader.next()

            if len(header) == 1:
                reader = csv.reader(f, delimiter=',')
                header = header[0].split(',')

            csv_content = [ns(dict(zip(header, row))) for row in reader if row[0]]

        return csv_content

    def create_contact_address(self, O, petition):
        contract_id = None
        try:
            contract_id = get_last_contract_on_cups(O, petition.cups)
        except:
            error = "This cups did not have any previous contract in somenergia"
            raise Exception(error)

        partner_id, _ = O.GiscedataPolissa.read(contract_id, ['titular'])['titular']

        country_id = O.ResCountry.search([('code','like','ES')])[0]
        new_partner_address_id, created  = get_or_create_partner_address(
            O,
            partner_id=partner_id,
            street='Adreça electronica - ' + petition.compte_email,
            postal_code=petition.titular_cp,
            city_id=int(petition.titular_municipi),
            state_id=petition.titular_provincia,
            country_id=country_id,
            email=petition.compte_email,
            phone=''
        )


    def create_employees(self, filename):
        O = Client(**configdb.erppeek_odoo)
        employee_lines = self.read_employees_data_csv(filename)

        for employee_data in employee_lines:
            print(employee_data)
            user_id = 0
            partner_id = 0

            # CREATE PARTNER
            state_id = O.ResCountryState.search([('name','=',employee_data['provincia'].decode('utf8'))], context={'lang':'ca_ES'})
            partner_data = {
                'firstname': employee_data['nom'].decode('utf8'),
                'lastname': employee_data['cognoms'].decode('utf8'),
                #'name': employee_data['cognoms'] + ", " + employee_data['nom'],
                'street': employee_data['carrer'].decode('utf8'),
                'city': employee_data['poblacio'].decode('utf8'),
                'state_id': state_id,
                'country_id': 68,
                'zip': employee_data['codi_postal'],
                'mobile': employee_data['num_mobil'],
                'phone': employee_data['num_fix'],
                'email': employee_data['email'],
                'vat': employee_data['dni'],
            }
            try:
                if O.ResPartner.search([('vat','=',employee_data['dni'])]):
                    raise Exception("Partner already exist")
                partner_id = O.ResPartner.create(partner_data)
                success("Partner created: {}", partner_data['email'])
            except Exception as e:
                msg = "I couldn\'t create a new partner {}, reason {}"
                warn(msg, empleat_data, e)

            # CREATE PARTNER ADDRESS: Not necessary anymore


            # CREATE USER
            import pudb;pu.db
            # Get groups_ids
            groups = employee_data['permisos'].split(',')
            groups_id = []
            for group in groups:
                group_id = O.ResGroups.search([('full_name','=',group)])
                if not group_id:
                    warn("Grup no trobat {}", group.decode('utf8'))
                else:
                    groups_id.append(group_id[0])
            # Create user
            user_data = {
                'firstname': employee_data['nom'].decode('utf8'),
                'lastname': employee_data['cognoms'].decode('utf8'),
                'login': employee_data['email'],
                'groups_id': groups_id,
                'password': 'odoo',
                'lang': 'ca_ES',
                'tz': 'Europe/Andorra',
                'sel_groups_1_9_10': 1,
                'action_id': 191, #Attendance
                'partner_id': partner_id
            }
            try:
                if O.ResUsers.search([('login','=',employee_data['email'])]):
                    raise Exception("User already exist")
                user_id = O.ResUsers.create(user_data)
                # Add user to a group
                for group in groups_id:
                    O.ResGroups.write(group, {'users': [(4, user_id.id)]})
                success("User created: {}", employee_data['email'])
            except Exception as e:
                msg = "I couldn\'t create a new user {}, reason {}"
                warn(msg, user_data, e)


            # CREATE EMPLOYEE
            # Get department id
            team_id = O.HrDepartment.search([('complete_name','=',employee_data['equips'].decode('utf8'))], context={'lang':'ca_ES'})
            if not team_id:
                warn("Equip no trobat {}", employee_data['equips'])
                continue
            # Get jornada
            jornada_id = 1
            if employee_data['jornada'] == '40':
                jornada_id = O.IrModelData.get_object_reference('somenergia','resource_calendar_som_40h_partida')[1]
            elif employee_data['jornada'] == '35':
                jornada_id = O.IrModelData.get_object_reference('somenergia','resource_calendar_som_35h')[1]
            elif employee_data['jornada'] == '32':
                jornada_id = O.IrModelData.get_object_reference('somenergia','resource_calendar_som_32h_dll_div')[1]

            empleat_data = {
                'name': employee_data['cognoms'].decode('utf8') + ", " + employee_data['nom'].decode('utf8'),
                'identification_id': employee_data['dni'],
                'work_email': employee_data['email'],
                'department_id': team_id,
                'gender': employee_data['genere'],
                'user_id': user_id,
                'resource_calendar_id': jornada_id,
                'birthday':  datetime.strftime(datetime.strptime(employee_data['data_neixement'], "%d/%m/%Y"), "%Y-%m-%d"),
                'theoretical_hours_start_date': '2021-04-01',
            }
            try:
                if O.HrEmployee.search([('identification_id','=',employee_data['dni'])]):
                    raise Exception("Employee already exist")
                employee_id = O.HrEmployee.create(empleat_data)
                success("Employee created: {}", empleat_data['name'])
            except Exception as e:
                msg = "I couldn\'t create a new empoyee {}, reason {}"
                warn(msg, empleat_data, e)





def main(csv_file):
    impd = ImportData()
    impd.create_employees(csv_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Custom import Employees from csv Script'
    )

    parser.add_argument(
        '--file',
        dest='csv_file',
        required=True,
        help="csv with employees data"
    )

    args = parser.parse_args()
    try:
        main(args.csv_file)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        error("Process failed: {}", str(e))
    else:
        success("Finished!")
