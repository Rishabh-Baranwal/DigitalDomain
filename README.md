Approach:

CLI:
Used class structure for defining the CLI and initialising with the arguments
provided and then calling the run method which takes care of all the operations
bassed on the input parameters/arguments. No two operation can be done
simultaneously. For parsing the arguments, argparse library/package has been
used.

API:
Used functional structure in order to carry out different operations. The run
method from CLI calls the appropriate method based on the input parameters.

Create function built the parent level structure till the type, for child
level helper method is being called recursively based on the datatype of the
field value. If the value is of string type then its a leaf node, no more
child inside it else if it is of type dict then called itself recursively
until it hits the leaf node.

List(listing type) function lists the projects which are present in
the project folder, optionally filters over the type(s) provided. Used
listdir inbuilt function to list the project.

Types(listing project) function lists the type in the project. Used listdir
inbuilt function to list the types in the project.

Delete function tries to delete the project if no dcc type provided otherwise
type will be checked in the project and then that dcc type will be deleted.
This operation fails if the folder which needs to be deleted is not empty or
not having proper permission to delete. Added one forceful argument in case
user wants to delete forcefully.

Describe function describes the project structure using the walk inbuilt
function.
