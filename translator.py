
import json
import copy
import traceback

from typing import TypeVar, Union, NoReturn

class DocumentTranslator:
    '''
    WHAT IS DOCUMENT TRANSLATOR ?
    document translator class translates sequential document with context handler & instance handler
    also, provides built in functions on global context based on variable "built_in_functions" 

    sequential document format
        - id (str)                 : unique instance id
        - display (str)            : instance display name
        - expression (str)         : python expression
        - is_global_context (bool) : execution flag on global context
        - next_id (str)            : next unique instance id
        - contains (list)          : instances that are contained

    built in functions
        - _copy_this_context                    : copy current context deeply to other context
        - _copy_variable_from_context           : copy variable deeply from other context to current context
        - _refer_this_context                   : reference current context to other context
        - _refer_variable_from_context          : reference variable from other context to current context (mutable object)
        - _globalize_variable_from_this_context : set variable from current context in global context
        - _raise_exception                      : raise exception with sequential document format
    '''

    def __init__(self, context_handler_class: TypeVar('ContextHandler'), instance_handler_class: TypeVar('InstanceHandler')):
        self.__context_handler = context_handler_class()
        self.__instance_handler = instance_handler_class()
        
        self.__stacked = []
        self.__current_instance = None
        self.__trigger_id = '__trigger__'

        self.built_in_functions = [
            '_copy_this_context',
            '_copy_variable_from_context',
            '_refer_this_context',
            '_refer_variable_from_context',
            '_globalize_variable_from_this_context',
            '_raise_exception'
            ]

    @property
    def context_handler(self):
        return self.__context_handler

    @property
    def instance_handler(self):
        return self.__instance_handler

    @property
    def stacked(self):
        return self.__stacked

    @property
    def current_instance(self):
        return self.__current_instance
        
    def __copy_local_context(self, source_local_key, destination_local_key):
        self.__context_handler[destination_local_key] = copy.deepcopy(self.__context_handler[source_local_key])
        return None

    def __copy_variable(self, source_local_key, destination_local_key, variable):
        self.__context_handler[destination_local_key][variable] = copy.deepcopy(self.__context_handler[source_local_key][variable])
        return None

    def __refer_local_context(self, source_local_key, destination_local_key):
        self.__context_handler[destination_local_key] = self.__context_handler[source_local_key]
        return None

    def __refer_variable(self, source_local_key, destination_local_key, variable):
        self.__context_handler[destination_local_key][variable] = self.__context_handler[source_local_key][variable]
        return None

    def __globalize_variable(self, local_key, variable):
        self.__context_handler[self.__context_handler.global_key][variable] = self.__context_handler[local_key][variable]
        return None

    def __raise_exception(self, exception):
        exception_instance_id = self.current_instance[self.__instance_handler.KEY_ID]
        exception_instance_display = self.current_instance[self.__instance_handler.KEY_DISPLAY]
        exception_line_number = traceback.extract_tb(exception.__traceback__)[-1][1]
        message = '[exception from instance id "{0}", display "{1}", line {2}] {3}'.format(
            exception_instance_id,
            exception_instance_display,
            exception_line_number,
            str(exception)
            )

        raise type(exception)(message).with_traceback(exception.__traceback__) from None
    
    def _copy_this_context(self, destination_local_key: str) -> NoReturn:
        return self.__copy_local_context(self.current_instance[self.__instance_handler.KEY_ID], destination_local_key)

    def _copy_variable_from_context(self, source_local_key: str, variable: str) -> NoReturn:
        return self.__copy_variable(source_local_key, self.current_instance[self.__instance_handler.KEY_ID], variable)
    
    def _refer_this_context(self, destination_local_key: str) -> NoReturn:
        return self.__refer_local_context(self.current_instance[self.__instance_handler.KEY_ID], destination_local_key)

    def _refer_variable_from_context(self, source_local_key: str, variable: str) -> NoReturn:
        return self.__refer_variable(source_local_key, self.current_instance[self.__instance_handler.KEY_ID], variable)

    def _globalize_variable_from_this_context(self, variable: str) -> NoReturn:
        return self.__globalize_variable(self.current_instance[self.__instance_handler.KEY_ID], variable)

    def _raise_exception(self, exception: Exception) -> NoReturn:
        return self.__raise_exception(exception)

    def _translate_instance(self, instance: TypeVar('Sequential Document')) -> Union[TypeVar('Sequential Document'), NoReturn]:
        instance_id                 = instance[self.__instance_handler.KEY_ID]
        instance_display            = instance[self.__instance_handler.KEY_DISPLAY]
        instance_expression         = instance[self.__instance_handler.KEY_EXPRESSION]
        instance_is_global_context  = instance[self.__instance_handler.KEY_IS_GLOBAL_CONTEXT]
        instance_next_id            = instance[self.__instance_handler.KEY_NEXT_ID]
        instance_contains           = instance[self.__instance_handler.KEY_CONTAINS]
        
        self.__current_instance = instance
        self.__stacked.append(instance_id)

        if instance_id not in self.__context_handler._get_context_keys():
            self.__context_handler._set_local_context(instance_id)
        
        if instance_expression:
            try:
                if instance_is_global_context:
                    self.__context_handler._exec_is_global_context(instance_expression)

                else:
                    self.__context_handler._exec_on_local_context(instance_expression, instance_id)
            
            except Exception as exception:
                self._raise_exception(exception)

        if len(instance_contains) > 0:
            return self.__instance_handler._get_instance_case_enter_contains(instance)

        elif instance_next_id:
            return self.__instance_handler._get_instance_case_general(instance)

        elif self.__instance_handler.instance_to_do is not None:
            return self.__instance_handler._get_instance_case_break_contains(instance)
        
        else:
            return None
        
    def translate(self, serialized_document: str) -> NoReturn:
        document = json.loads(serialized_document)

        self.__context_handler._set_global_context()
        self.__context_handler._set_built_in_functions(self, self.built_in_functions)
        self.__instance_handler._resolve_as_instance(document)

        has_instance_to_do = True
        instance = self.__instance_handler.instance_container[self.__trigger_id]
        
        while has_instance_to_do:
            instance = self._translate_instance(instance)
            has_instance_to_do = instance != None
        
        return None
