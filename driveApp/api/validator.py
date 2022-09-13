from driveApp.db.utils import importData


class ValidateSystemItemImport:
    def __init__(self, data):
        self.data = data
        self.d = {}
        self.ids = []

    @staticmethod
    async def is_folder(path):
        res = await importData.is_folder_db(path)
        if res is None:
            return True  # TODO: PIZDA DODELAt
        else:
            return False

    async def __validateSourceFormat(self) -> (bool, dict):
        if type(self.data) != dict:
            return False, {'code': 400, 'message': 'Incorrect data type. (Remained dict)'}

        if 'items' not in self.data.keys():
            return False, {'code': 400, 'message': "No key items in data!"}

        if type(self.data['items']) != list:
            return False, {'code': 400, 'message': 'Incorrect data type. (Remained list)'}

        if 'updateDate' not in self.data.keys():
            return False, {'code': 400, 'message': "No key updateData in data!"}
        return True, {}

    async def __validateItemJsonStruct(self) -> (bool, dict):
        if type(self.d) != dict:
            return False, {'code': 400, 'message': "Incorrect data type. (Remained dict)"}

        if 'id' not in self.d.keys() or 'url' not in self.d.keys() or 'parentId' not in self.d.keys() or 'size' not in self.d.keys() or 'type' not in self.d.keys():
            return False, {'code': 400, 'message': f"Validation Failed!\nNot all parameters passed\nElement: {self.d}"}
        return True, {}

    async def __validateId(self) -> (bool, dict):
        if self.d['id'] in self.ids:
            return False, {'code': 400,
                           'message': f'Validation Failed!\nOne request cannot have two elements with the same id\nElement: {self.d}'}

        if self.d['id'] is None or type(self.d['id']) != str:
            return False, {"code": 400, "message": f"Validation Failed!\nIncorrect ID value for the element {self.d}"}
        self.ids.append(self.d['id'])
        return True, {}

    async def __validateUrl(self) -> (bool, dict):
        if self.d['type'] == "FOLDER" and self.d['url'] is not None:
            return False, {'code': 400,
                           "message": f"Validation Failed!\nUrl field should always be null when importing a folder\nElement: {self.d}"}

        if len(self.d['url']) > 255 and self.d['type'] == "FILE":
            return False, {'code': 400,
                           'message': f"Validation Failed!\nThe size of the url field when importing a file must always be less than or equal to 255\nElement: {self.d}"}
        return True, {}

    async def __validateParentId(self) -> (bool, dict):
        return True, {} # TODO: родителем элемента может быть только папка, принадлежность к папке определяется полем parentId, элементы могут не иметь родителя (при обновлении parentId на null элемент остается без родителя)

    async def __validateSize(self) -> (bool, dict):
        if self.d['size'] is not None and self.d['type'] == "FOLDER":
            return False, {'code': 400,
                           'message': f"Validation Failed!\nThe size field must always be null when importing a folder\nElement: {self.d}"}

        if self.d['type'] == "FILE" and self.d['size'] <= 0:
            return False, {'code': 400,
                           'message': "Validation Failed!\nThe size field for files must always be greater than 0\nElement: {d}"}
        return True, {}

    async def __validateType(self) -> (bool, dict):
        if self.d['type'] != "FOLDER" and self.d['type'] != "FILE":
            return False, {'code': 400, 'message': f"Validation Failed!\nIncorrect type value.\nElement: {self.d}"}
        return True, {}

    async def __validateDate(self) -> (bool, dict):
        # try:
        #     datetime.datetime.strptime(data['updateDate'], '%Y-%m-%dT%H%:M%:S.%fZ')
        # except ValueError:
        #     print(data['updateDate'])
        #     return {"code": 400, "message": f"Validation Failed!\nDate processed according to ISO 8601\nElement: {d}"}  TODO: проверить ебучую дату
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

        for d in self.data['items']:
            self.d = d
            tests = [
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
