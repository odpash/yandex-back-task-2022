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
        if "type" in self.__d.keys():
            if not (await self.__validateType())[0]:
                return await self.__validateType()
        else:
            return False, {'code': 400, "message": f"Validation Failed!\nNot all parametrs passed\nElement: {self.__d}"}

        if self.__d['type'] == 'FILE':
            if 'id' not in self.__d.keys() or 'url' not in self.__d.keys() or 'parentId' not in self.__d.keys() or 'size' not in self.__d.keys() or 'type' not in self.__d.keys():
                return False, {'code': 400,
                               'message': f"Validation Failed!\nNot all parameters passed\nElement: {self.__d}"}
        else:
            if 'id' not in self.__d.keys() or 'parentId' not in self.__d.keys():
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
        if self.__d['type'] == "FOLDER" and self.__d.get('url') is not None:
            return False, {'code': 400,
                           "message": f"Validation Failed!\nUrl field should always be null when importing a folder\nElement: {self.__d}"}

        if self.__d['type'] == "FILE" and len(self.__d.get('url')) > 255:
            return False, {'code': 400,
                           'message': f"Validation Failed!\nThe size of the url field when importing a file must always be less than or equal to 255\nElement: {self.__d}"}
        return True, {}

    async def __validateParentId(self) -> (bool, dict):
        has_father = False
        for element in self.__database_info:
            if element[0] == self.__d['parentId'] and element[2] == 'FILE':
                return False, {"code": 400, "message": f"Validation Failed!\nThe parent can only be a folder (belonging to the parentId field of the folder decision)\nElement: {self.__d}"}
            if element[0] == self.__d['parentId']:
                has_father = True

        if not has_father and self.__d['parentId'] is not None:
            return False,  {'code': 400, 'message': f'Validation Failed!\nObject has no father in struct\nElement: {self.__d}'}
        return True, {}

    async def __validateSize(self) -> (bool, dict):
        if self.__d.get('size') is not None and self.__d['type'] == "FOLDER":
            return False, {'code': 400,
                           'message': f"Validation Failed!\nThe size field must always be null when importing a folder\nElement: {self.__d}"}

        if self.__d['type'] == "FILE" and self.__d.get('size') <= 0:
            return False, {'code': 400,
                           'message': "Validation Failed!\nThe size field for files must always be greater than 0\nElement: {d}"}
        return True, {}

    async def __validateType(self) -> (bool, dict):
        if self.__d['type'] != "FOLDER" and self.__d['type'] != "FILE":
            return False, {'code': 400, 'message': f"Validation Failed!\nIncorrect type value.\nElement: {self.__d}"}
        return True, {}

    async def __validateDate(self) -> (bool, dict):
        try:
            datetime.datetime.fromisoformat(self.__data['updateDate'].replace('Z', '+00:00'))
        except:
            return {"code": 400,
                    "message": f"Validation Failed!\nDate processed according to ISO 8601\nElement: {self.__d}"}
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
            status, error = await self.__validateItemJsonStruct()
            if not status:
                return error

            try:
                tests = [
                    await self.__validateDate(),
                    await self.__validateId(),
                    await self.__validateUrl(),
                    await self.__validateParentId(),
                    await self.__validateSize()
                ]
            except Exception as e:
                tests = []
                print(e, "ERROR")
            # -->  Check if all tests are passed  <-- #
            for test in tests:
                if not test[0]:
                    return test[1]
            # <--  -----------------------------  --> #

            # --> Add to database <-- #
            try:
                is_in_db = False
                for i in range(len(self.__database_info)):
                    if self.__d['id'] == self.__database_info[i][0]:
                        is_in_db = True
                        if self.__d['type'] != self.__database_info[i][2]:
                            return {'code': 400, f'message': 'Not supported operation to change file type!'}
                        self.__database_info[i] = (self.__d['id'], self.__d['parentId'], self.__d['type'])
                if not is_in_db:
                    self.__database_info.append((self.__d['id'], self.__d['parentId'], self.__d['type']))
            except Exception as e:
                print("ERROR", e)
            # <== --------------- <-- #



        return {'code': 200, "message": "OK"}
