import requests
import re
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator


def translate_text(smth):
  # split the text into smaller chunks of 5000 characters
  chunks = [smth[i:i+4000] for i in range(0, len(smth), 4000)]
  # translate each chunk and join them together
  translated = ""
  for chunk in chunks:
    translated += GoogleTranslator(source='auto', target='ru').translate(chunk)
  return translated


def import_acc(passw):
  headers = {
      'X-Password': passw,
      'User-Agent': 'vkwhfiuwe',
  }
  response = requests.get('https://www.nationstates.net/cgi-bin/api.cgi?nation=Maria-Ra&q=issues', headers=headers)
  text_def = response.text
  #print(text)
  return text_def


def take_form():
  global optionID, issueID, issue_id
  print('Введите id вашего ответа:')
  optionID = str(input())
  issueID = issue_id
  send_answer(issueID, optionID, "Stas.2005")
  take_issue()

def send_answer(issueID, optionID,passw):
  # create a URL string with the NationStates API endpoint
  url = "https://www.nationstates.net/cgi-bin/api.cgi"

  # create a data dictionary with the required parameters
  data = {
    "nation": "Maria-Ra",
    "c": "issue",
    "issue": issueID,
    "option": optionID
  }

  # create a headers dictionary with the password and user agent
  headers = {
    "X-Password": passw,
    "User-Agent": "sobolevstas82@gmail.com"
  }

  # make a POST request to the URL with the data and headers
  response = requests.post(url, data=data, headers=headers)

  # return the text of the response as a string
  return response.text


def full_text():
  global text
  text = import_acc('Stas.2005')


def get_issue(xml_text, issue_id):
  pattern = r'<ISSUE id="{}">(.*?)</ISSUE>'.format(issue_id)
  issue_match = re.search(pattern, xml_text, flags=re.DOTALL)
  if issue_match is None:
    return None
  title_match = re.search(r'<TITLE>(.*?)</TITLE>', issue_match.group(1))
  text_match = re.search(r'<TEXT>(.*?)</TEXT>', issue_match.group(1))
  option_matches = re.findall(r'<OPTION id="(\d+)">(.*?)</OPTION>', issue_match.group(1), flags=re.DOTALL)
  options = {option_id: option_text.strip() for option_id, option_text in option_matches}
  issue = {
    'title': title_match.group(1).strip(),
    'text': text_match.group(1).strip(),
    'options': options
  }
  return issue


def error(issue,_id):
  global agree
  if issue is not None:
      print('Title:', translate_text(issue['title']))
      print('Text:', translate_text(issue['text']))
      print('Options:')
      for option_id, option_text in issue['options'].items():
          print(translate_text(f'{option_id}: {option_text}'))
      print('Желаете ответить (да/нет)?')
      agree = str(input())
      if agree == 'да' or agree == 'Да':
        take_form()
      else:
        return take_issue()

  else:
    print(f'Проблема {_id} не найдена.')



def get_all_titles(xml_text):
  pattern = r'<ISSUE id="(\d+)">\s*<TITLE>(.*?)</TITLE>'
  matches = re.findall(pattern, xml_text, flags=re.DOTALL)
  titles = [f'{match[0]}: {match[1]}' for match in matches]
  return '\n'.join(titles)


def all_tile():
  print(translate_text(get_all_titles(text)))


def take_issue():
  global issue_id
  full_text()
  all_tile()
  # Define an id to look for
  print('Введите id вопроса')
  issue_id=str(input())
  issue = get_issue(text, issue_id)
  error(issue,issue_id)

take_issue()




