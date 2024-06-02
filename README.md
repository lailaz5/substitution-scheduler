# substitution-scheduler
"substitution-scheduler" is a project born from the idea of digitally managing substitutions within the institution. 
It is a project based on React, where the frontend is implemented using this library along with JavaScript for API interaction and dynamic components within the pages. The backend is developed in Python and includes scraping the schedule page from the institution's website, configuring the database, and various API endpoints.

The assignment of substitutions is not automated, but the program handles extracting and classifying information (obtained through scraping or from management documents) related to the teacher to be replaced, providing a series of compatible options. These options are selected based on criteria such as favoring the choice of a teacher from the same class council, belonging to the same disciplinary area, etc.

This solution aims to significantly simplify the work of school staff, enabling a quick and accurate distribution of human resources in case of unforeseen circumstances.
