[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 5b8673b..f721652 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -4,7 +4,6 @@[m
 *serv.md[m
 *__pycache__[m
 *.vercel[m
[31m-*.venv[m
 .fauna[m
 archived[m
 node_modules[m
[1mdiff --git a/server/app.py b/server/app.py[m
[1mindex d8c8bbd..d8a01f6 100644[m
[1m--- a/server/app.py[m
[1m+++ b/server/app.py[m
[36m@@ -67,13 +67,12 @@[m [mdef elected_members():[m
 ### Elected Member ###[m
 @app.route("/elected_member")[m
 def elected_member():[m
[31m-  return "Error 500: Internal error. Endpoint to be implemented soon.", 500[m
[31m-  # name = request.args.get('name')[m
[31m-  # if not name:[m
[31m-  #   return "name not found", 400[m
[31m-  # object = getDataFaunaIndex("elected_member_ref_by_name", name)[m
[31m-  # object['contributions'] = getDataFaunaIndex("contributions_ref_by_elected_member", name)[m
[31m-  # return object[m
[32m+[m[32m  # return "Error 500: Internal error. Endpoint to be implemented soon.", 500[m
[32m+[m[32m  name = request.args.get('name')[m
[32m+[m[32m  if not name:[m
[32m+[m[32m    return "name not found", 400[m
[32m+[m[32m  object = getDataFaunaIndex("elected_member_ref_by_name", name)[m
[32m+[m[32m  return object[m
 [m
 ### Dates ###[m
 @app.route("/dates")[m
