
class ContextHandler:
    '''
    WHAT IS CONTEXT HANDLER ?
    context handler class handles contexts safely when executing expression,  
    and local context key is based on instance's id (so each instance would be gueranteed independence)
    but global context key is limited to variable "__global_key"
    REMEMBER! CANNOT ACCESS MAIN CONTEXT FROM EACH SUB CONTEXT (GLOBAL & LOCAL)
    
    main context : document translation runtime
        - global context : global context made by context handler from main context
        - local context 01 : an independent local context made by context handler from main context
    '''

    def __init__(self):
        self.__global_key = '__gcontext__'
        self.__context_container = {}

    @property
    def context_container(self):
        return self.__context_container

    @property
    def global_key(self):
        return self.__global_key

    def __setitem__(self, key, value):
        self.__context_container[key] = value

    def __getitem__(self, key):
        return self.__context_container[key]

    def __repr__(self):
        return repr(self.__context_container)

    def __str__(self):
        return str(self.__context_container)

    def _set_built_in_functions(self, from_class, built_in_functions):
        for built_in_function in built_in_functions:
            self.__context_container[self.__global_key][built_in_function] = getattr(from_class, built_in_function)

    def _get_context_keys(self):
        return self.__context_container.keys()

    def _set_global_context(self):
        self.__context_container[self.__global_key] = {}

    def _set_local_context(self, local_key):
        self.__context_container[local_key] = {}

    def _exec_is_global_context(self, expression):
        exec(expression, self.__context_container[self.__global_key], None)

    def _exec_on_local_context(self, expression, local_key):
        exec(expression, self.__context_container[self.__global_key], self.__context_container[local_key])

class InstanceHandler:
    '''
    WHAT IS INSTANCE HANDLER ?
    instance handler class resolves sequential document as instance,
    handles execution flow sequentially, 
    and also provides essential keys to tranlate instance
    '''

    KEY_ID = 'id'
    KEY_DISPLAY = 'display'
    KEY_EXPRESSION = 'expression'
    KEY_IS_GLOBAL_CONTEXT = 'is_global_context'
    KEY_NEXT_ID = 'next_id'
    KEY_CONTAINS = 'contains'

    def __init__(self):
        self.__instance_container = {}
        self.__instance_to_do = None

    def __repr__(self):
        return repr(self.__instance_container)

    def __str__(self):
        return str(self.__instance_container)

    @property
    def instance_container(self):
        return self.__instance_container

    @property
    def instance_to_do(self):
        return self.__instance_to_do

    def __setitem__(self, key, value):
        self.__instance_container[key] = value

    def __getitem__(self, key):
        return self.__instance_container[key]

    def __repr__(self):
        return repr(self.__instance_container)

    def __str__(self):
        return str(self.__instance_container)

    def _resolve_as_instance(self, document):
        self.__instance_container[document[self.__class__.KEY_ID]] = document
        for sub_document in document[self.__class__.KEY_CONTAINS]:
            self._resolve_as_instance(sub_document)

    def _get_instance_case_general(self, instance):
        return self.__instance_container[instance[self.__class__.KEY_NEXT_ID]]

    def _get_instance_case_enter_contains(self, instance):
        if instance[self.__class__.KEY_NEXT_ID]:
            self.__instance_to_do = self.__instance_container[instance[self.__class__.KEY_NEXT_ID]]

        return self.__instance_container[instance[self.__class__.KEY_CONTAINS][0][self.__class__.KEY_ID]]

    def _get_instance_case_break_contains(self, instance):
        if self.instance_to_do is not None: 
            instance_to_do = self.__instance_to_do
            self.__instance_to_do = None
            return instance_to_do
        
        else:
            return None