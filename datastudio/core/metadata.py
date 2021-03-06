#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : Data Studio                                                       #
# Version : 0.1.0                                                             #
# File    : metadata.py                                                       #
# Python  : 3.8.1                                                             #
# --------------------------------------------------------------------------- #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/datastudio                     #
# --------------------------------------------------------------------------- #
# Created       : Friday, February 14th 2020, 8:47:19 am                      #
# Last Modified : Sunday, February 16th 2020, 7:04:22 am                      #
# Modified By   : John James (jjames@decisionscients.com>)                    #
# --------------------------------------------------------------------------- #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
""" Management of administrative, descriptive, tech and process metadata.

This module encapsulates the creation, management, and reporting of 
administrative, descriptive, tech and process metadata, hereinafter
called the metadata taxonomy. The classes include:

    * Metadata : Main class containing the metadata taxonomy objects.    
    * AbstractMetadataFactory : Interface for the MetadataFactory class
    * DataSetMetadataFactory : Constructs the DataSet MetaData object.
    * DataSourceFileMetadataFactory : DataSourceFile Metadata    
    * AbstractMetadata : Interace for metadata taxonomy classes.
    * MetadataAdmin : Data and behaviors for administrative metadata
    * MetadataDesc : Data and behaviors for descriptive metadata
    * MetadataTech : Data and behaviors for tech metadata
    * MetadataDatabase : Data and behaviors for database metadata
    * MetadataProcess : Data and behaviors for process metadata

TODO: Create factorys for supported RDBMS DataSource objects.

"""
from abc import ABC, abstractmethod, abstractproperty
import os
from datetime import datetime
from collections import OrderedDict
import platform
from pprint import pprint
import psutil
import sys
import time
import uuid

from ..utils.format import scale_number
# --------------------------------------------------------------------------- #
#                                 Metadata                                    #
# --------------------------------------------------------------------------- #
class Metadata:
    """ Class containing administrative, descriptive, and tech metadata."""

    def __init__(self):
        self._metadata = {}

    def add(self, metadata):          
        """Adds metadata object.
        
        Parameters
        ----------
        metadata : A MetadataAdmin, MetadataDesc, or MetadataTech object        
        """      
        self._metadata[metadata.metadata_type.lower()] = metadata

    def get(self, metadata_type=None):
        """ Returns a metadata object.

        Returns the administrative, descriptive, technical or process metadata 
        object based upon a partial match of the metadata_type parameter.  

        Parameters
        ----------
        metadata_type : str
            String or partial string containing the type of metadata.
        """
        if metadata_type is None:
            return self._metadata
        else:
            metadata = next(v for (k, v) in self._metadata.items() if \
                metadata_type.lower() in k.lower())
            if metadata:
                return metadata
            else:
                raise KeyError("No metadata type matching '{t}'. \
                    Run the 'print_types' method for a list of supported \
                        metadata types.".format(t=metadata_type))

    def print_types(self):
        for k in self._metadata.keys():
            print(k)

    def print(self, metadata_type=None):
        if metadata_type:
            metadata = next(v for (k, v) in self._metadata.items() if \
                metadata_type.lower() in k.lower())
            metadata.print()

        else:            
            for v in self._metadata.values():
                v.print()



# --------------------------------------------------------------------------- #
#                          AbstractMetadataFactory                            #
# --------------------------------------------------------------------------- #
class AbstractMetadataFactory(ABC):
    """Abstract base class exposing methods for creating the Metadata objects."""

    def __init__(self, entity, name, **kwargs):
        self._entity = entity
        self._name = name
        self._addl_params = {}
        self._addl_params.update(kwargs)
        self._reset()

    def _reset(self):
        self._metadata = Metadata()   

    @property
    def metadata(self):
        """ Returns the metadata object once completed."""
        metadata = self._metadata
        self._reset()
        return metadata             

    @abstractmethod
    def create_admin(self):
        pass

    @abstractmethod
    def create_desc(self):
        pass

    @abstractmethod
    def create_tech(self):
        pass

    @abstractmethod
    def create_process(self):
        pass


# --------------------------------------------------------------------------- #
#                        MetadataEntityFactory                                #
# --------------------------------------------------------------------------- #
class MetadataEntityFactory(AbstractMetadataFactory):
    """ Builds a Metadata object for DataSet objects."""

    def __init__(self, entity, name, **kwargs):        
        """ Fresh creator object should contain an empty Metadata object."""
        super(MetadataEntityFactory, self).__init__(entity, name, **kwargs)

    def create_admin(self):
        """Adds a administrative metadata subclass object."""
        admin = MetadataAdmin(self._entity, self._name, **self._addl_params)
        self._metadata.add(admin)

    def create_desc(self):
        """Adds a descriptive metadata subclass object."""
        desc = MetadataDesc(self._entity, self._name, **self._addl_params)
        self._metadata.add(desc)

    def create_tech(self):
        """Adds a tech metadata subclass object."""
        tech = MetadataTech(self._entity, self._name, **self._addl_params)
        self._metadata.add(tech)

    def create_process(self):
        """Adds a process metadata subclass object."""
        process = MetadataProcess(self._entity, self._name, **self._addl_params)
        self._metadata.add(process)


# --------------------------------------------------------------------------- #
#                       MetadataDataCollectionFactory                         #
# --------------------------------------------------------------------------- #
class MetadataDataCollectionFactory(AbstractMetadataFactory):
    """ Builds a Metadata object for DataCollection objects."""

    def __init__(self, entity, name, **kwargs):        
        """ Fresh creator object should contain an empty Metadata object."""
        super(MetadataDataCollectionFactory, self).__init__(entity, name, **kwargs)

    def create_admin(self):
        """Adds a administrative metadata subclass object."""
        admin = MetadataAdmin(self._entity, self._name, **self._addl_params)
        self._metadata.add(admin)

    def create_desc(self):
        """Adds a descriptive metadata subclass object."""
        desc = MetadataDescDataCollection(self._entity, self._name, **self._addl_params)
        self._metadata.add(desc)

    def create_tech(self):
        """Adds a tech metadata subclass object."""
        tech = MetadataTech(self._entity, self._name, **self._addl_params)
        self._metadata.add(tech)

    def create_process(self):
        """Adds a process metadata subclass object."""
        process = MetadataProcess(self._entity, self._name, **self._addl_params)
        self._metadata.add(process)


# --------------------------------------------------------------------------- #
#                          MetadataFileFactory                                #
# --------------------------------------------------------------------------- #
class MetadataFileFactory(AbstractMetadataFactory):
    """ Builds a Metadata object for DataSourceFile objects."""

    def __init__(self, entity, name, **kwargs):        
        """ Fresh creator object should contain an empty Metadata object."""
        super(MetadataFileFactory, self).__init__(entity, name, **kwargs)

    def create_admin(self):
        """Adds a administrative metadata subclass object."""
        admin = MetadataAdminFile(self._entity, self._name, **self._addl_params)
        self._metadata.add(admin)

    def create_desc(self):
        """Adds a descriptive metadata subclass object."""
        desc = MetadataDesc(self._entity, self._name, **self._addl_params)
        self._metadata.add(desc)

    def create_tech(self):
        """Adds a tech metadata subclass object."""
        tech = MetadataTechFile(self._entity, self._name, **self._addl_params)
        self._metadata.add(tech)

    def create_process(self):
        """Adds a process metadata subclass object."""
        process = MetadataProcess(self._entity, self._name, **self._addl_params)
        self._metadata.add(process)

# --------------------------------------------------------------------------- #
#                           MetadataRDBMSFactory                              #
# --------------------------------------------------------------------------- #
class MetadataRDBMSFactory(AbstractMetadataFactory):
    """ Builds a Metadata object for RDBMS based DataSource and DataStore objects."""

    def __init__(self, entity, name, **kwargs):        
        """ Fresh creator object should contain an empty Metadata object."""
        super(MetadataRDBMSFactory, self).__init__(entity, name, kwargs)

    def create_admin(self):
        """Adds a administrative metadata subclass object."""
        admin = MetadataAdmin(self._entity, self._name, **self._addl_params)
        self._metadata.add(admin)

    def create_desc(self):
        """Adds a descriptive metadata subclass object."""
        desc = MetadataDesc(self._entity, self._name, **self._addl_params)
        self._metadata.add(desc)

    def create_tech(self):
        """Adds a tech metadata subclass object."""
        tech = MetadataTechRDBMS(self._entity, self._name, **self._addl_params)
        self._metadata.add(tech)

    def create_process(self):
        """Adds a process metadata subclass object."""
        process = MetadataProcess(self._entity, self._name, **self._addl_params)
        self._metadata.add(process)

# --------------------------------------------------------------------------- #
#                           MetadataRemoteFactory                             #
# --------------------------------------------------------------------------- #
class MetadataRemoteFactory(AbstractMetadataFactory):
    """ Builds a Metadata object for DataSourceDB and DataStorageDB objects."""

    def __init__(self, entity, name):        
        """ Fresh creator object should contain an empty Metadata object."""
        self._entity = entity
        self._name = name
        self._reset()

    def _reset(self):
        self._metadata = Metadata()

    @property
    def metadata(self):
        """ Returns the metadata object once completed."""
        metadata = self._metadata
        self._reset()
        return metadata

    def create_admin(self):
        """Adds a administrative metadata subclass object."""
        admin = MetadataAdminURL(self._entity, self._name, **self._addl_params)
        self._metadata.add(admin)

    def create_desc(self):
        """Adds a descriptive metadata subclass object."""
        desc = MetadataDesc(self._entity, self._name, **self._addl_params)
        self._metadata.add(desc)

    def create_tech(self):
        """Adds a tech metadata subclass object."""
        tech = MetadataTech(self._entity, self._name, **self._addl_params)
        self._metadata.add(tech)

    def create_process(self):
        """Adds a process metadata subclass object."""
        process = MetadataProcess(self._entity, self._name, **self._addl_params)
        self._metadata.add(process)        

# --------------------------------------------------------------------------- #
#                           AbstractMetadata                                  #
# --------------------------------------------------------------------------- #
class AbstractMetadata(ABC):
    """ Abstract base class for adminstrative, descriptive, & tech metadata.""" 

    def __init__(self, entity, name, **kwargs):
        self._entity = entity
        self._metadata = OrderedDict() 

    def update(self, event=None):
        """Updates metadata attributes to reflect changes to object."""
        self._metadata['updates'] += 1

    def get(self, key=None):
        """Returns the value for a specific attribute."""
        if key:
            if key in self._metadata:
                return self._metadata.get(key, None)
            else:
                raise KeyError("Key, '{key}', does not exist.".format(key=key))
        else:
            return self._metadata.copy()

    def add(self, key, value):
        """Adds metadata attribute."""
        if key not in self._metadata:
            self._metadata[key] = value
        else:
            raise ValueError("Key {key} already exists.".format(key=key))

    def change(self, key, value):
        """Change a key value pair."""
        if key not in self._metadata:
            raise KeyError("Key {key} does not exist.".format(key=key))
        else:
            self._metadata[key] = value

    def remove(self, key):
        """Remove a key value pair based upon 'key'."""
        try:
            del self._metadata[key]
        except KeyError:
            print("Key {key} does not exist.".format(key=key))     

    def print(self):
        """Prints the metadata."""
        pprint(self._metadata)       

# --------------------------------------------------------------------------- #
#                            MetadataAdmin                                    #
# --------------------------------------------------------------------------- #
class MetadataAdmin(AbstractMetadata):
    """Abstract base class for all administrative metadata objects."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataAdmin, self).__init__(entity, name, **kwargs)
        self.metadata_type = 'Administrative'

        # Extract user datetime and object data once to avoid repeated calls.
        user = os.getlogin()
        date = datetime.now()
        date_string = str(date.year) + '-' + str(date.month) + '-' + \
            str(date.day) + '_' + str(date.hour) + '-' + str(date.minute) + '-' \
                + str(date.second)
        date_formatted = time.strftime("%c")
        classname = entity.__class__.__name__
        
        self._metadata['id'] = str(uuid.uuid4())
        self._metadata['name'] = name
        self._metadata['creator'] = user
        self._metadata['created'] = date_formatted
        self._metadata['modifier'] = user
        self._metadata['modified'] = date_formatted
        self._metadata['updates'] = 0
        self._metadata['classname'] = classname        
        self._metadata['objectname'] = user.lower() + '_' + date_string + '_' + '_'\
            + classname.lower() + '_' + name.lower()

    def update(self, event=None):
        """Updates metadata attributes to reflect changes to object."""
        super(MetadataAdmin, self).update()
        self._metadata['modifier'] = os.getlogin()
        self._metadata['modified'] = time.strftime("%c")
        self._metadata['updates'] += 1

# --------------------------------------------------------------------------- #
#                          MetadataAdminFile                                  #
# --------------------------------------------------------------------------- #
class MetadataAdminFile(MetadataAdmin):        
    """Administrative metadata for DataSourceFile and DataStorageFile objects."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataAdminFile, self).__init__(entity, name, **kwargs)       
        path = kwargs.get('path', None)                
        if path:
            self._metadata['path'] = path
            self._metadata['directory'] = os.path.dirname(path)
            self._metadata['filename'] = os.path.basename(path)
            self._metadata['fileext'] = os.path.splitext(path)[1]
            self._metadata['file_exists'] = os.path.exists(path)
            self._metadata['file_created'] = time.strftime("%c", \
                time.localtime(os.path.getctime(path)))
            self._metadata['file_last_accessed'] = time.strftime("%c", \
                time.localtime(os.path.getatime(path)))                
            self._metadata['file_last_modified'] = time.strftime("%c", \
                time.localtime(os.path.getmtime(path)))                           


# --------------------------------------------------------------------------- #
#                          MetadataAdminURL                                   #
# --------------------------------------------------------------------------- #
class MetadataAdminURL(MetadataAdmin):  
    """Metadata for remote data sources."""

    _params = ['url']

    def __init__(self, entity, name, **kwargs):
        super(MetadataAdminURL, self).__init__(entity, name, **kwargs)      
        url = dict(filter(lambda item: 'url' in item[0], self._metadata.items()))        
        self._metadata.update(url)
    
# --------------------------------------------------------------------------- #
#                              MetadataDesc                                   #
# --------------------------------------------------------------------------- #
class MetadataDesc(AbstractMetadata):
    """ Storage and management of descriptive metadata."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataDesc, self).__init__(entity, name, **kwargs)
        self.metadata_type = 'Descriptive'
        self._metadata['type'] = "" # User defined type
        self._metadata['category'] = "" # User defined category 
        self._metadata['title'] = ""  # Capital case title for the object
        self._metadata['description_short'] = "" # One line description         
        self._metadata['description'] = "" # Long description
        self._metadata['class'] = entity.__class__.__name__
        self._metadata['version'] = "0.1.0"
       
# --------------------------------------------------------------------------- #
#                          MetadataDescDataCollection                         #
# --------------------------------------------------------------------------- #
class MetadataDescDataCollection(MetadataDesc):  
    """Metadata for DataCollection objects."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataDescDataCollection, self).__init__(entity, name, **kwargs)      
        self._reset()


    def _reset(self):
        self._metadata['n_members'] = 0
        self._metadata['n_members_datacollection'] = 0
        self._metadata['n_members_dataset'] = 0


    def update(self, event=None):      
        """Updates collection counts.""" 
        self._reset()
        
        for k, v in self._entity.get().items():
            self._metadata['n_members'] += 1
            if v.__class__.__name__ == 'DataCollection':            
                self._metadata['n_members_datacollection'] += 1
            else:
                self._metadata['n_members_dataset'] += 1
        

# --------------------------------------------------------------------------- #
#                              MetadataTech                                   #
# --------------------------------------------------------------------------- #
class MetadataTech(AbstractMetadata):
    """ Storage and management of tech metadata."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataTech, self).__init__(entity, name, **kwargs)
        self.metadata_type = 'Technical'

        self._format_metadata()        

    def update_metadata(self, event=None):
        """ Updates metadata and increments the number of updates."""
        self._format_metadata()
        super(MetadataTech, self).update()        

    def _format_metadata(self):    
        """Formats tech metadata."""        
        uname = platform.uname()
        svmem = psutil.virtual_memory()

        self._metadata['system'] = uname.system
        self._metadata['node'] = uname.node
        self._metadata['release'] = uname.release
        self._metadata['version'] = uname.version
        self._metadata['machine'] = uname.machine
        self._metadata['processor'] = uname.processor
        self._metadata['release'] = uname.release
        self._metadata['physical_cores'] = psutil.cpu_count(logical=False)
        self._metadata['total_cores'] = psutil.cpu_count(logical=True)
        self._metadata['total_memory'] = scale_number(svmem.total)
        self._metadata['available_memory'] = scale_number(svmem.available)
        self._metadata['used_memory'] = scale_number(svmem.used)
        self._metadata['pct_memory_used'] = svmem.percent        
        self._metadata['object_size'] = sys.getsizeof(self._entity)


# --------------------------------------------------------------------------- #
#                          MetadataTechFile                                   #
# --------------------------------------------------------------------------- #
class MetadataTechFile(MetadataTech):
    """ Additional metadata for DataSourceFile and DataStoreFile classes."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataTechFile, self).__init__(entity, name, **kwargs) 
        path = kwargs.get('path', None)        
        if path:        
            self._metadata['file_size'] = scale_number(os.path.getsize(path), "M")         

# --------------------------------------------------------------------------- #
#                          MetadataTechRDBMS                                  #
# --------------------------------------------------------------------------- #
class MetadataTechRDBMS(MetadataTech):        
    """Technical metadata for RDBMS sources and storage objects."""

    _params = ['database', 'user', 'password', 'host', 'port']

    def __init__(self, entity, name, **kwargs):
        super(MetadataTechRDBMS, self).__init__(entity, name, **kwargs)       
        rdbms_params = dict(filter(lambda item: item[0] in self._params, kwargs.items()))                
        self._metadata.update(rdbms_params)
   

# --------------------------------------------------------------------------- #
#                              MetadataProcess                                #
# --------------------------------------------------------------------------- #
class MetadataProcess(AbstractMetadata):
    """ Storage and management of process metadata."""

    def __init__(self, entity, name, **kwargs):
        super(MetadataProcess, self).__init__(entity, name, **kwargs)
        self.metadata_type = 'Process'      

        self._metadata['log'] = []

        user = os.getlogin()
        date_formatted = time.strftime("%c")
        classname = entity.__class__.__name__        
        msg = classname + " object named '" + name + "' was instantiated " +\
            ' at ' + date_formatted + ' by ' + user + '.'
        self._metadata['log'].append(msg)

    def update(self, event=None):
        """Logs an activity update.""" 
        user = os.getlogin()
        date_formatted = time.strftime("%c")
        classname = self._entity.__class__.__name__        
        msg = 'Class : ' + classname + 'Name : ' + self._name +\
            'Date : ' + date_formatted + 'Event : ' + event
        if event:
            self._metadata['log'].append(msg)

    def print(self):
        for e in self._metadata['log']:
            print(e)
