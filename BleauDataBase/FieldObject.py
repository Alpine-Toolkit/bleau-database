####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

class Field:

    """This class defines a field by its name and factory."""

    ##############################################

    def __init__(self, name, factory):

        self.name = name
        self.factory = factory

####################################################################################################

class InstanceChecker:

    """Factory to check the type of an instance object."""

    ##############################################

    def __init__(self, cls):

        self._cls = cls

    ##############################################

    def __call__(self, obj):

        if isinstance(obj, self._cls):
            return obj
        else:
            raise ValueError("Object {} must be of type {}".format(str(type(obj)), self._cls))

####################################################################################################

class StringList(list):

    """Factory to check a string list."""

    ##############################################

    def __init__(self, *args):

        super().__init__([str(x) for x in args])

####################################################################################################

class FromJsonMixinMetaClass(type):

    """This metaclass lookup for fields."""

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        type.__init__(cls, class_name, super_classes, class_attribute_dict)

        fields = {}
        for attribute, obj in class_attribute_dict.items():
            if not attribute.startswith('__') and isinstance(obj, (type, InstanceChecker)):
                fields[attribute] = Field(attribute, obj)
        cls.__fields__ = fields
        cls.__field_names__ = sorted([field for field in fields])

####################################################################################################

class FromJsonMixin(metaclass=FromJsonMixinMetaClass):

    """This mixin class implements the import/export to JSON."""

    __fields__ = {}
    __field_names__ = []

    ##############################################

    def __init__(self, raise_for_unknown=True, **kwargs):

        # Set and check given fields
        for key, value in kwargs.items():
            if key not in self.__field_names__:
                if raise_for_unknown:
                    raise ValueError('Unknown key {}'.format(key))
                else:
                    continue
            factory = self.__fields__[key].factory
            # print(key, value, factory)
            if value is not None:
                if isinstance(value, dict):
                    value = factory(**value)
                elif isinstance(value, list):
                    value = factory(*value)
                else:
                    value = factory(value)
            setattr(self, key, value)
        
        # Set to None missing fields
        for key in self.__field_names__:
            if key not in kwargs:
                setattr(self, key, None)

    ##############################################

    def str_long(self):

        return '\n'.join(['{}: {}'.format(field, self.__dict__[field])]
                         for field in self.__field_names__)

    ##############################################

    def to_json(self, only_defined=False, exclude=()):

        # Fixme: rename __json_interface__ ?

        d = {}
        for field in self.__field_names__:
            if field not in exclude:
                value = self.__dict__[field]
                if hasattr(value, '__json_interface__'):
                    value = value.__json_interface__
                if not only_defined or value is not None:
                    d[field] = value
        
        return d

####################################################################################################
#
# End
#
####################################################################################################
