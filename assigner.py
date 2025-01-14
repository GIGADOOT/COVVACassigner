
from jira import JIRA, JIRAError
from jira.resources import Comment
import requests
import keyboard

# Подключение и аутентификация
authData123 = open("creds.txt", 'r')
authDataRead = authData123.read()

jira_address = "https://jira.mos.social"

jira_user = authDataRead.split('LOGIN:')[1]
jira_user = jira_user.split('\nPASSWORD:')[0]

jira_password = authDataRead.split('PASSWORD:')[1]
jira_password = jira_password.split('\nEPIC:')[0]

jira_epic = authDataRead.split('EPIC:')[1]
jira = JIRA(server=jira_address, basic_auth=(jira_user, jira_password))

# Получение списка задач
jqlRequest = 'project = COVIDVAC and assignee = currentUser() AND text ~ "сверить данные"'
listOfJiraIssues = jira.search_issues(jqlRequest)

# Назначение на автора задачи и добавление комментария
print('Введите номер ЗНИ, полученный в письме о выполнении работ')
zni = input()
comment = "Выполнено в рамках ЗНИ № "

for issue in listOfJiraIssues:
    if issue:
        issue.update(fields={'customfield_10101': jira_epic})
        #jira.add_comment(issue, f'{comment}{zni}', visibility={'type': 'role', 'value': 'Developers'})
        #jira.add_worklog(issue, '5m')
        jira.transition_issue(issue, transition='11') #11 - взять в работу
        jira.transition_issue(issue, transition='5') #5 - resolved
        key = issue.key
        assignee = issue.fields.assignee.key
        reporter = issue.fields.reporter.name
        jira.assign_issue(key, reporter)
        print(f"Данные обновлены в задаче {key}")

print('Нажмите ENTER для выхода...')
keyboard.read_event('enter')
