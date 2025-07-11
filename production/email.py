from production.tasks import send_notification_mail
import logging
from datetime import datetime

class EmailBuild():
    def __init__(self, version_data):
        self.version_data = version_data

    def on_approve_email_build(version_data=None):
        if version_data:
            # print(version_data[0]['shot'])
            context = {
                "client": version_data[0]['shot']['sequence']['project']['client']['name'],
                "project": version_data[0]['shot']['sequence']['project']['name'],
                "sequence": version_data[0]['shot']['sequence']['name'],
                "shot": version_data[0]['shot']['name'],
                "task_type": version_data[0]['shot']['task_type']['name'],
                "version": version_data[0]['version'],
                "output_path": version_data[0]['output_path'],
                "submission_notes": version_data[0]['submission_notes'],
                "verified_by":version_data[0]['sent_by']['fullName'],
                "verfied_date":version_data[0]['sent_date']
            }
            if version_data[0]['shot']['sequence']['project']['client']['name'] == "ISP":
                if version_data[0]['shot']['naming_check']:
                    context.update(naming_check='Passed')
                    # template = "./email_templates/approve_email_naming_sucess_template.html"
                    template = "./email_templates/approve_email_naming_sucess_template.html"
                else:
                    context.update(naming_check='Not Passed')
                    template = "./email_templates/approve_email_naming_error_template.html"
            else:
                template = "./email_templates/approve_email_template.html"
            subject = "Upload Shot: "+ version_data[0]['shot']['sequence']['project']['client']['name']+"_"+version_data[0]['shot']['sequence']['project']['name']+"-"+version_data[0]['shot']['task_type']['name']+":"+version_data[0]['shot']['name']
            to_addr = ['IO@pixrock.org']
            reply_to = [version_data[0]['sent_by']['email']]
            cc_addr = ['narendar@pixrock.org']
            if version_data[0]['shot']['location']['name'] == "CHENNAI":
                cc_addr.extend(['PC1063_Aishwarya@pixrock.org','shotbuzzalerts@pixrock.org'])
            else:
                if version_data[0]['shot']['task_type']['name'] == "PAINT":
                    cc_addr.extend(['psc1167_Ilayaraja@PIXROCK.ORG','ps1175_soniya@pixrock.org'])
                elif version_data[0]['shot']['task_type']['name'] == "ROTO":
                    cc_addr.extend(['ps1007_Ayyarkannan@PIXROCK.ORG','ps1270_keerthiga@pixrock.org'])
                elif version_data[0]['shot']['task_type']['name'] == "MM":
                    cc_addr.extend(['ps1269_sasi@pixrock.org'])
                # elif version_data[0]['shot']['task_type']['name'] == "COMP":
                #     cc_addr.extend(['ramarao.k@oscarfx.com'])
                if version_data[0]['sent_by'] is not None and version_data[0]['sent_by']['email'] is not None and version_data[0]['sent_by']['email'] not in cc_addr:
                    cc_addr.append(version_data[0]['sent_by']['email'])
                if version_data[0]['shot']['team_lead'] is not None and version_data[0]['shot']['team_lead']['email'] is not None and version_data[0]['shot']['team_lead']['email'] not in cc_addr:
                    cc_addr.append(version_data[0]['shot']['team_lead']['email'])
                if version_data[0]['shot']['supervisor'] is not None and version_data[0]['shot']['supervisor']['email'] is not None and version_data[0]['shot']['supervisor']['email'] not in cc_addr:
                    cc_addr.append(version_data[0]['shot']['supervisor']['email'])
                cc_addr.extend(['shotbuzzalerts@pixrock.org'])

            try:
                logging.info("Initiated Email for shot: {}".format(version_data[0]['shot']['name']) )
                send_notification_mail(context=context,template=template,subject=subject, to_addr=to_addr, cc_addr=cc_addr, reply_to=reply_to)
            except Exception as e:
                logging.error("Error for shot: {}".format(version_data[0]['shot']['name']))
                logging.error(e)
                # print(e)