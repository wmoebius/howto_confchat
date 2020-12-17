import requests
import pandas as pd
import unidecode

def u2h(str):
    # there must be a smarter way to do this?
    return str.encode('ascii', 'xmlcharrefreplace').decode(encoding='utf-8')

# token and userid for meeadmin
token = 'GETINROCKETCHAT'
userid = 'GETINROCKETCHAT'

# read in list of attendees
df = pd.read_csv('attendees.csv')

# https://docs.rocket.chat/api/rest-api/methods/users/create
# https://curl.trillworks.com/#python
headers = {
    'X-Auth-Token': token,
    'X-User-Id': userid,
    'Content-type': 'application/json',
}

fmm = open('formailmerge.csv','w')
fmm.write('email,fullnamesimple,username\n')

flp = open('listparticipants.html.txt','w')

df.sort_values(by=['Registrant-name'], inplace=True)

for index, row in df.iterrows():

    # gather data
    fullname = row['Registrant-name'].rstrip()
    fullnamesimple = unidecode.unidecode(fullname)
    # create username
    username = fullnamesimple.lower().replace('. ','.').replace(' ','.').replace('\'','-')
    name = fullnamesimple
    email = row['Registrant-email']
    #   if fullname!=fullnamesimple:
    #       print(name+' '+email+' '+username+'\n')

    # check if user exists
    params = ( ('username', username), )
    response = requests.get('https://chat.meevirtual.org/api/v1/users.info', headers=headers, params=params)

    if response.json()['success']:
         # write existing user info into csv file
         fmm.write(email+','+fullnamesimple+','+username+'\n')
    else:
        # create new user

        # format for API
        data = '{"name": "vname", "email": "vemail", "password": "meevirtualpassword", "username": "vusername", '
        data = data + '"requirePasswordChange": true, "sendWelcomeEmail": true}'
        data = data.replace('vname',name).replace('vemail',email).replace('vusername',username)

        # create user
        response = requests.post('https://chat.meevirtual.org/api/v1/users.create', headers=headers, data=data)

        if response.json()['success']:
            print('Success!')
        else:
            print(data)
            print('No success!')

    flp.write('<tr><td>'+u2h(fullname)+'</td><td>'+username+'</td></tr>\n')

flp.close()
fmm.close()
