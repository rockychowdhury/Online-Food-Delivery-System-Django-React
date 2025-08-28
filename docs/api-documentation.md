Food :
GET     api/foods                   Public
GET     api/foods/res               Public
POST    api/foods                   RO, BM                      |   Admin, Cu, RS, DP, SS
PUT     api/foods                   RO, BM                      |   Admin, Cu, RS, DP, SS
PATCH   api/foods                   RO, BM, RS                  |   Admin, Cu, DP, SS
DELETE  api/foods                   RO, BM, Admin               |   Cu, DP, SS, RS

Restaurant :

GET api/restaurants                 Public
GET api/restaurants/:id             Public
GET api/restaurants/branches        public


Branch :
GET api/branches                    Public

Menu:

Order :
GET     api/orders                  Admin, SS, RO, BM, RS, Cu   |   DP
POST    api/orders                  RO, BM                      |   Admin, Cu, RS, DP, SS
PUT     api/orders                  RO, BM                      |   Admin, Cu, RS, DP, SS
PATCH   api/orders                  RO, BM, RS                  |   Admin, Cu, DP, SS
DELETE  api/orders                  RO, BM, Admin               |   Cu, DP, SS, RS
