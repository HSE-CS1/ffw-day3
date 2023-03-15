from flask import json

# utility functions
def update_json(filename, data):
  with open(filename, "w") as file:
    json.dump(data, file, indent=2)
    

# this function will load all the 
# members from my members.json file
def load_members():
  with open("members.json") as file:
    MEMBERS = json.load(file)

  return MEMBERS

def get_member(email):
  """This function will check if a member exists and return their index
  and the member dict. If the member does not exist then it will return None"""
  MEMBERS = load_members() # get the current list of members
  #loop through the list of MEMBERS and look for a matching email
  for index, member in enumerate(MEMBERS):
    if member.get("email") == email: #found a matching email
      return index, member
  return -1, None # -1 for index, and None for member


def add_member(new_member):
  MEMBERS = load_members() # get the current list of members
  MEMBERS.append(new_member)  # add the new member to the list
  # update the json file with the new data
  update_json("members.json", MEMBERS)
  return MEMBERS.index(new_member) # return the index of the new member


def get_member_by_index(ind):
  #get the current MEMBERS list
  MEMBERS = load_members()
  #check to make sure the index passed in is in 
  #the range of members
  if ind < 0 or ind > len(MEMBERS) - 1:
    return None
  return MEMBERS[ind]

def update_member_information(ind, member):
  # get the current MEMBERS
  MEMBERS = load_members()
  MEMBERS[ind].update(member) # update the member info
  # update the json file
  update_json("members.json", MEMBERS)