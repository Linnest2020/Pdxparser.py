"""
 Paradox language parser in Python

Enjoy.

@ author Linnest2020
"""

from typing import Dict, List, Tuple, Union,Container


class PdxParser:
    """
     Paradox language parser in Python

    Enjoy.
    """
    def __init__(self,text) -> None:
        self.ambigouous = []
        self.text = text
    def parse(self,start=0) -> Union[Tuple[Union[Dict,List],int],Union[Dict,List]]:
        """
        parse: Parse the text

        enjoy it

        :param start: start index, defaults to 0
        :type start: int, optional
        :return: return the dict `obj` in default,
        if `obj` is empty return the list `key_stack`,
        if the start greater than 0, also return current id to make the id move away.
        :rtype: Union[Tuple[Union[Dict,List],int],Union[Dict,List]]
        """
        obj = {}
        key_stack = []
        key = ""
        value = ""
        value_walk = False
        is_comment = False
        meet_blank = False
        index = start
        while index < len(self.text):
            if self.text[index] == "#":
                is_comment = True
            if self.text[index] in "\r\n" and is_comment:
                is_comment = False
                value_walk = False
                meet_blank = False
                key = ""
                value = ""
            if not is_comment:
                if self.text[index] in "\t \r\n" or index == len(self.text)-1:
                    if self.text[index] not in "\t \r\n":
                        if value_walk and not self.text[index] == "}":
                            value += self.text[index]
                        elif not value_walk and not self.text[index] == "}":
                            key += self.text[index]
                        if meet_blank or not value:
                            key_stack.append(key)
                            key = ""
                            meet_blank = False
                    elif key and self.text[index] in "\t \r\n":
                        if index == len(self.text)-1:
                            key_stack.append(key)
                        meet_blank = True

                    if value_walk and value and key_stack[-1]:
                        if isinstance(obj[key_stack[-1]],list): # add value
                            if not obj[key_stack[-1]][-1]:
                                obj[key_stack[-1]][-1] = value
                            elif isinstance(obj[key_stack[-1]][-1],list) and \
                                obj[key_stack[-1]][-1][0] in "!=>=<=" and \
                                    not obj[key_stack[-1]][-1][-1]:
                                obj[key_stack[-1]][-1][-1] = value
                            else:
                                obj[key_stack[-1]].append(value)
                        else:
                            obj[key_stack[-1]] = value
                        value = ""
                        value_walk = False
                    if self.text[index] == "}":
                        if key:
                            key_stack.append(key)
                        res = obj if obj else key_stack
                        return res,index
                elif self.text[index] == "}" and index > 0:
                    if key:
                        key_stack.append(key)
                    if value_walk and value and key_stack[-1]:
                        if isinstance(obj[key_stack[-1]],list):
                            if not obj[key_stack[-1]][-1]:
                                obj[key_stack[-1]][-1] = value
                            elif isinstance(obj[key_stack[-1]][-1],list) and \
                                obj[key_stack[-1]][-1][0] in "!=>=<=" and \
                                    not obj[key_stack[-1]][-1][-1]:
                                obj[key_stack[-1]][-1][-1] = value
                            else:
                                obj[key_stack[-1]].append(value)
                        else:
                            obj[key_stack[-1]] = value
                        value = ""
                        value_walk = False
                    res = obj if obj else key_stack
                    return res,index
                elif self.text[index] == "{":
                    value_walk = True
                    block_value,block_id = self.parse(start=index+1)
                    index = block_id
                    if isinstance(obj[key_stack[-1]],list):
                        if not obj[key_stack[-1]][-1]:
                            obj[key_stack[-1]][-1] = block_value
                        else:
                            obj[key_stack[-1]].append(block_value)
                    else:
                        obj[key_stack[-1]] = block_value
                    value_walk = False
                elif self.text[index] in ">=<!":
                    operator = self.text[index]
                    if self.text[index] in ">!<":
                        if self.text[index+1] == "=":
                            operator += self.text[index+1]
                            index += 1
                    key_stack.append(key)

                    cur_node = None
                    if operator != "=":
                        cur_node = [operator,None]
                        value_walk = True

                    if obj.get(key):
                        if key not in self.ambigouous:
                            self.ambigouous.append(key)
                            tmp_node = obj[key]
                            obj[key] = [tmp_node,cur_node]
                        else:
                            if isinstance(obj[key],list):
                                obj[key].append(cur_node)
                            else:
                                tmp_node = obj[key]
                                obj[key] = [tmp_node,cur_node]
                    else:
                        obj[key] = cur_node
                    if not obj[key] or not obj[key][-1] :
                        value_walk = True
                    key = ""
                elif self.text[index] not in "\t \r\n":
                    if not value_walk:
                        if meet_blank:
                            key_stack.append(key)
                            key = ""
                            meet_blank = False
                        key += self.text[index]
                    else:
                        value += self.text[index]
            index += 1
        return obj if obj else key_stack


class Pdxwriter:# inspired by jomini.js
    """
     Paradox language writer in Python
     inspired by jomini.js

    Enjoy.
    """
    def __init__(self) -> None:
        self.layer = 0
        self.text = ""
        self.is_array = False
        self.is_key = True
        self.operator = "="
    def tabbed_write(self):
        """
        tabbed_write
        """
        self.text += self.layer*"  "
    def write_header(self,header:Union[str,int,float]):
        """
        write_header make header like rgb{0.1 0.1 0.1}

        :param header: header before {}
        :type header: Union[str,int,float]
        """
        self.tabbed_write()
        self.text +=  str(header)
    def write_string(self,string:Union[str,int,float]):
        """
        write_string Write key or value

        :param string: Key if key, value if value, array if array
        :type string: Union[str,int,float]
        """
        if self.is_key:
            self.tabbed_write()
            self.text += str(string)
            self.is_key = not self.is_key
        elif self.is_array:
            self.text += " " + str(string)
        else:
            self.text += self.operator + str(string) + "\n"
            self.is_key = not self.is_key
    def op_reset(self):
        """
        op_reset reset operator as "="
        """
        self.operator = "="
    def any_start(self):
        """
        any_start start with {
        """
        self.text += "{\n"
        self.layer += 1
    def end(self):
        """
        end end with }
        """
        self.is_array = False
        self.is_key = True
        self.layer -= 1
        self.tabbed_write()
        self.text += "}\n"
    def array_end(self):
        """
        array_end end, but add "\\n"
        """
        self.text += "\n"
        self.end()
    def array_start(self):
        """
        array_start start, but marked as array

        """
        self.text += self.operator
        self.is_array = True
        self.any_start()
        self.tabbed_write()
    def object_start(self):
        """
        object_start start, marked as object(Dict)
        """
        self.text += self.operator
        self.any_start()
        self.is_key = True
    def dump_one_block(self,
        key:Union[str,int,float],
        value:Union[str,int,float,List,Dict],
        ambigouous:Container[str]=()) -> str:
        """
        dump_one_block Dump one block(i.e, key=value)

        :param key: key of a block
        :type key: Union[str,int,float]
        :param value: any value of a block
        :type value: Union[str,int,float,List,Dict]
        :param ambigouous: ambigouous keys, defaults to ()
        :type ambigouous: Container[str], optional
        :return: the stringfy of one block
        :rtype: str
        """
        if isinstance(value,list) and key in ambigouous:
            if not isinstance(value[0],dict):
                for item in value:
                    self.write_string(key)
                    if not isinstance(item,list):
                        self.write_string(item)
                    elif item[0] in ">=<=!=":
                        self.operator = item[0]
                        self.write_string(item[1])
                        self.op_reset()
            elif isinstance(value[0],dict):
                for item in value:
                    self.write_string(key)
                    self.object_start()
                    for item_key,item_value in item.items():
                        self.dump_one_block(item_key,item_value,ambigouous)
                    self.end()
        elif isinstance(value,list):
            self.write_string(key)
            if value[0] in ">=<=!=":
                self.operator = value[0]
                self.write_string(value[1])
                self.op_reset()
            else:
                self.array_start()
                for item in value:
                    if not isinstance(item,list) and not isinstance(item,dict):
                        self.write_string(item)
                    elif isinstance(item,dict):
                        self.object_start()
                        for item_key,item_value in item.items():
                            self.dump_one_block(item_key,item_value,ambigouous)
                        self.end()
                self.array_end()
        elif not isinstance(value,dict):
            self.write_string(key)
            self.write_string(value)
        else:
            self.write_string(key)
            self.object_start()
            for item_key,item_value in value.items():
                self.dump_one_block(item_key,item_value,ambigouous)
            self.end()
        return self.text
    def dump(self,pdxinput:Union[Dict,PdxParser],ambigouous:Container[str]=()) -> str:
        """
        dump Dump in classical

        _extended_summary_

        :param pdxinput: And be PdxParser or Dict
        :type pdxinput: Union[Dict,PdxParser]
        :param ambigouous: ambigouous keys, defaults to ()
        :type ambigouous: Container[str], optional
        :return: text of a pdxinput
        :rtype: str
        """
        if isinstance(pdxinput,PdxParser):
            pdxdict = pdxinput.parse()
            ambigouous = pdxinput.ambigouous
        elif isinstance(pdxinput,dict):
            pdxdict = pdxinput
        for key,value in pdxdict.items():
            self.dump_one_block(key,value,ambigouous)
        return self.text


if __name__ == "__main__":
    TEST = "some_trigger = { AND = {a>b a<=c a!=d a = e a >= f a !=g} } "
    PP = PdxParser(TEST)
    pdx_dict = PP.parse()
    print("TEST:",TEST)
    print("==========")
    print("Parse output: ",pdx_dict)
    pdxwriter = Pdxwriter()
    dump_test = pdxwriter.dump(pdx_dict,PP.ambigouous)
    print("Dump: ",dump_test)
    pdx_reparse_dict = PdxParser(dump_test).parse()
    print("Reparse comparing, Older is Newer?: ",pdx_reparse_dict == pdx_dict)
