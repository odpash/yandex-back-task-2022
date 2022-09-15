import datetime


class SystemItemImportValidator:
    def __init__(self, data, database_info):
        self.__data = data
        self.__d = {}
        self.__ids = []
        self.__database_info = database_info

    async def __validateSourceFormat(self) -> (bool, dict):
        if type(self.__data) != dict:
            return False, {'code': 400, 'message': 'Incorrect data type. (Remained dict)'}

        if 'items' not in self.__data.keys():
            return False, {'code': 400, 'message': "No key items in data!"}

        if type(self.__data['items']) != list:
            return False, {'code': 400, 'message': 'Incorrect data type. (Remained list)'}

        if 'updateDate' not in self.__data.keys():
            return False, {'code': 400, 'message': "No key updateData in data!"}
        return True, {}

    async def __validateItemJsonStruct(self) -> (bool, dict):
        if type(self.__d) != dict:
            return False, {'code': 400, 'message': "Incorrect data type. (Remained dict)"}

        if 'id' not in self.__d.keys() or 'url' not in self.__d.keys() or 'parentId' not in self.__d.keys() or 'size' not in self.__d.keys() or 'type' not in self.__d.keys():
            return False, {'code': 400,
                           'message': f"Validation Failed!\nNot all parameters passed\nElement: {self.__d}"}
        return True, {}

    async def __validateId(self) -> (bool, dict):
        if self.__d['id'] in self.__ids:
            return False, {'code': 400,
                           'message': f'Validation Failed!\nOne request cannot have two elements with the same id\nElement: {self.__d}'}

        if self.__d['id'] is None or type(self.__d['id']) != str:
            return False, {"code": 400, "message": f"Validation Failed!\nIncorrect ID value for the element {self.__d}"}
        self.__ids.append(self.__d['id'])
        return True, {}

    async def __validateUrl(self) -> (bool, dict):
        if self.__d['type'] == "FOLDER" and self.__d['url'] is not None:
            return False, {'code': 400,
                           "message": f"Validation Failed!\nUrl field should always be null when importing a folder\nElement: {self.__d}"}

        if len(self.__d['url']) > 255 and self.__d['type'] == "FILE":
            return False, {'code': 400,
                           'message': f"Validation Failed!\nThe size of the url field when importing a file must always be less than or equal to 255\nElement: {self.__d}"}
        return True, {}

    async def __validateParentId(self) -> (bool, dict):
        return True, {}  # TODO: родителем элемента может быть только папка, принадле   жность к папке определяется полем parentId, элементы могут не иметь родителя (при обновлении parentId на null элемент остается без родителя)

    async def __validateSize(self) -> (bool, dict):
        if self.__d['size'] is not None and self.__d['type'] == "FOLDER":
            return False, {'code': 400,
                           'message': f"Validation Failed!\nThe size field must always be null when importing a folder\nElement: {self.__d}"}

        if self.__d['type'] == "FILE" and self.__d['size'] <= 0:
            return False, {'code': 400,
                           'message': "Validation Failed!\nThe size field for files must always be greater than 0\nElement: {d}"}
        return True, {}

    async def __validateType(self) -> (bool, dict):
        if self.__d['type'] != "FOLDER" and self.__d['type'] != "FILE":
            return False, {'code': 400, 'message': f"Validation Failed!\nIncorrect type value.\nElement: {self.__d}"}
        return True, {}

    async def __validateDate(self) -> (bool, dict):
        try:
            print(datetime.datetime.fromisoformat(self.__data['updateDate']))
        except:
            print("NO")
       # return {"code": 400, "message": f"Validation Failed!\nDate processed according to ISO 8601\nElement: {d}"} #  TODO: проверить ебучую дату
        return True, {}

    async def __validateDependencyTree(self) -> (bool, dict):
        return True, {}

    async def check(self) -> dict:
        """Public method used to check the correctness of the structure of the transferred data,
         their values and their compatibility with those already in the database
         INPUT: [{id, url, parentId, size, type}]
         OUTPUT: {code, message}
         """
        status, error = await self.__validateSourceFormat()
        if not status:
            return error

        for d in self.__data['items']:
            self.__d = d
            tests = [
                await self.__validateDate(),
                await self.__validateItemJsonStruct(),
                await self.__validateType(),
                await self.__validateId(),
                await self.__validateUrl(),
                await self.__validateParentId(),
                await self.__validateSize(),
                await self.__validateDependencyTree()
            ]

            # -->  Check if all tests are passed  <-- #
            for test in tests:
                if not test[0]:
                    return test[1]
            # <--  -----------------------------  --> #

        return {'code': 200, "message": "OK"}
