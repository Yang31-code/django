commands for this application：
##Only the commands shown below are valid

register
##You will be asked to enter username, password and email later.

login sc18x2y.pythonanywhere
##You will be asked to enter username and password later.

logout
##You should logout after you have already login, the token will expire after logout.

list
##Use this to list all module instances and professor(s) in a table.

view
##Use this to view the rating for all professors.

average professor_id module_code
##Use your args to replace professor_id and module_code, for example: "average JE1 CD1"

rate professor_id module_code year semester rating
##Replace the args, for example: "rate JE1 CD1 2018 2 5"
##you have to login before rating, and the number of rating should between 1 to 5
