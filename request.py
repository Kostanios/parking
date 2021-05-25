import requests
localURL = 'http://localhost:3000/create?nomer='
def pushNomer (nomer):
  try:
      print("server request: "+localURL+nomer)
      requests.post(localURL+nomer)
  except:
    print("server error with: "+localURL+nomer)