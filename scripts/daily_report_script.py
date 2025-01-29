import os
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import xlsxwriter

server = "http://10.10.10.10:8000"
token = '040734ca148cc9e7a62f2321e2238125204d6b80'
holidays = ['2025-01-01', '2025-01-14', '2025-03-14', '2025-04-01', '2025-08-15', '2025-08-27', '2025-10-02',
            '2025-10-20', '2025-12-25']
holidays = [datetime.strptime(date, '%Y-%m-%d') for date in holidays]
task_type_order = {'PAINT': 1, 'ROTO': 2, 'MM': 3}


def get_client_version(shot_id):
    return requests.get(f"{server}/api/production/client_versions/{shot_id}",
                        headers={'Authorization': f'Token {token}'}, verify=False).json()


def get_shot_data(shot_id):
    return requests.get(f"{server}/api/production/production_sheet/?shot_id={shot_id}",
                        headers={'Authorization': f'Token {token}'}, verify=False).json()[0]


# Ensure shots are populated correctly
def get_shot_history(from_date, to_date, toData):
    global shots  # Ensure we're using the global shots list
    shots = []  # Initialize shots as an empty list before populating
    v_dict = {}
    history_data = requests.get(f"{server}/api/history/shot/?from_date={from_date}&to_date={to_date}&toData={toData}",
                                headers={'Authorization': f'Token {token}'}, verify=False).json()

    for shot in history_data:
        shot_data = get_shot_data(shot['target'])
        c_ver = get_client_version(shot['target'])

        if shot_data['task_type'] not in v_dict:
            v_dict[shot_data['task_type']] = {}

        v_dict[shot_data['task_type']].setdefault(c_ver['version'], 0)
        v_dict[shot_data['task_type']][c_ver['version']] += 1

        # Add shot data to global shots list
        shots.append(shot_data)

    for task_type in v_dict:
        v_dict[task_type] = dict(sorted(v_dict[task_type].items()))

    return v_dict


def generate_html_table(v_dict):
    versions = sorted(set(version for task in v_dict.values() for version in task.keys()))
    column_totals = {version: 0 for version in versions}
    grand_total = 0

    table_html = "<table border='1' cellpadding='3' cellspacing='0' style='border-collapse: collapse;'>"
    table_html += "<tr style='background-color: #f78f40;'><th>Dept</th>" + "".join(
        f"<th>{version}</th>" for version in versions) + "<th>Grand Total</th></tr>"

    sorted_data = {task_type: v_dict[task_type] for task_type in
                   sorted(v_dict.keys(), key=lambda x: task_type_order.get(x, 4))}

    for task_type, versions_dict in sorted_data.items():
        row_total = 0
        table_html += f"<tr><td>{task_type}</td>"
        for version in versions:
            count = versions_dict.get(version, 0)
            row_total += count
            column_totals[version] += count
            table_html += f"<td>{count if count else ''}</td>"
        table_html += f"<td><b>{row_total}</b></td></tr>"
        grand_total += row_total

    table_html += "<tr><td><b>Grand Total</b></td>" + "".join(
        f"<td><b>{column_totals[version]}</b></td>" for version in versions)
    table_html += f"<td><b>{grand_total}</b></td></tr></table>"

    return table_html


def create_excel_file(file_name):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    border = workbook.add_format({'border': 1, 'border_color': 'black'})
    bold = workbook.add_format({'bold': True, 'bg_color': '#43d3f7', 'border': 1, 'border_color': 'black'})

    headers = ['CLIENT', 'PROJECT', 'SHOT', 'TASK', 'MAN DAYS', 'VERSION', 'SUPERVISOR', 'QC', 'CAPTAIN', 'ARTISTS',
               'COMMENTS']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold)

    row = 1
    for shot in sorted(shots, key=lambda x: (task_type_order.get(x['task_type'], 4), x['version'])):
        cli_ver = get_client_version(shot['id'])
        worksheet.write(row, 0, shot['sequence']['project']['client']['name'], border)
        worksheet.write(row, 1, shot['sequence']['project']['name'], border)
        worksheet.write(row, 2, shot['name'], border)
        worksheet.write(row, 3, shot['task_type'], border)
        worksheet.write(row, 4, shot['actual_bid_days'], border)
        worksheet.write(row, 5, shot['version'], border)
        worksheet.write(row, 6, shot['supervisor'], border)
        worksheet.write(row, 7, cli_ver['sent_by'], border)
        worksheet.write(row, 8, shot['artist'], border)
        worksheet.write(row, 9, ", ".join([artist['fullName'] for artist in shot['artists']]), border)
        row += 1

    worksheet.autofit()
    workbook.close()


def send_email(subject, body, to_email, cc, attachment_path=None):
    from_email = "vfx-pipeline@oscarfx.com"
    from_password = "slhm zvjt xbkj vqim"
    signature = """
    <br>----<br>
    Best regards,<br>
    Pipeline Team<br>
    <span style="color: grey;">
    <strong>**Disclaimer:**</strong><br>
    This is an automated email notification from ShotBuzz Automated Email System. Unauthorized use, disclosure, or copying is prohibited.
    </span>
    """
    msg = MIMEMultipart()
    msg['From'] = f'Shotbuzz Alerts <{from_email}>'
    msg['To'] = to_email
    msg['Cc'] = ', '.join(cc)
    msg['Subject'] = subject
    msg.attach(MIMEText(f"{body}<br><br>{signature}", 'html'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, [to_email] + cc, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def previous_working_date(today):
    yesterday = today - timedelta(days=1)

    while yesterday.weekday() == 6 or yesterday in holidays:
        yesterday -= timedelta(days=1)
    return yesterday

# Main execution flow
today = datetime.today()
yesterday = previous_working_date(today)

versions = get_shot_history(f"{yesterday.strftime('%Y-%m-%d')} 09:01", f"{today.strftime('%Y-%m-%d')} 09:00", "8")
html_table = generate_html_table(versions)


def main(to_email, cc):
    email_subject = f"Daily Retake Report_{today.strftime('%Y%m%d')}"
    if versions:
        attachment_path = f"/opt/jobs/Daily_Retake_Report_{today.strftime('%Y%m%d')}.xlsx"
        create_excel_file(attachment_path)
        email_body = f"<p>Dear Sir,</p><p> Please find the attached Daily retake report</p>{html_table}"
    else:
        email_body = "<p>Dear Sir,</p><p> Kindly note, there are no retakes received for today.</p>"
        attachment_path = None

    send_email(email_subject, email_body, to_email, cc, attachment_path)


# Define recipient and CC list
test = True
recipient = "narendar.ofx@gmail.com" if test else "kamalk@oscarfx.com"
cc_list = ['Narendar Reddy G <narendarreddy.gunreddy@oscarfx.com>'] if test else [
    'Narendar Reddy G <narendarreddy.gunreddy@oscarfx.com>',
    'praveeny.prod@oscarfx.com',
    'nareshp.prod@oscarfx.com',
    'monalisa@oscarfx.com',
    'laxmi.gidgi@oscarfx.com',
    'creative_roto@oscarfx.com',
    'creative_paint@oscarfx.com',
    'creative_mm@oscarfx.com',
    'creative_comp@oscarfx.com'
]

if test or (today.weekday() != 6 and today not in holidays):
    main(recipient, cc_list)
