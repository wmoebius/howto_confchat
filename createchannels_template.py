import subprocess

token = 'GETINROCKETCHAT'
userid = 'GETINROCKETCHAT'

listchannels = ['talk-YYY']

print(len(listchannels))

apicommand = "curl -H \"X-Auth-Token: token\" -H \"X-User-Id: userid\" -H \"Content-type: application/json\" "
apicommand = apicommand + "https://chat.meevirtual.org/api/v1/channels.create -d \'{ \"name\": \"channelname\" }\'"

for channelname in listchannels:
    thiscommand = apicommand.replace('token',token).replace('userid',userid).replace('channelname',channelname)
    print(thiscommand)
    returned_value=subprocess.call(thiscommand,shell=True)
    if returned_value!=0:
      sys.exit('Problem with creating channel.')
