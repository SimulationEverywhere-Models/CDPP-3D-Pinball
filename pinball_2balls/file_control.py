bl_info = {
    "name": "File_control.py",
    "author": "Colin Timmons",
    "version": (0,1),
    "blender": (2, 60, 0),
    "api": 41226,
    "location": "Ottawa, Ontario",
    "description": "Interface file script between the CD++ MA, VAL, and LOG files and the student's Blender python file.",
    "warning": "This file requires valid MA, LOG, the student's *.py and VAL file (if required) present with the Blend file",
    "wiki_url":""
    }

""" Comment field:
Name: 'CD++ Simulations Interface'
Blender: 2.60
Group: 'Simulations'
Tooltip: 'CD++ Simulations Interface Program'
"""

# --------------------------------------------------------------------------
#   # Copyright (C) 2011 Colin Timmons
#
#   This program is free software developed in house for SYSC 5104
#   Discrete Modelling and Simulation at Carleton University.

#   This program is free to distribute and or modify under the
#   terms of the applicable contract copyright laws for distribution
#   of the present country and under Canadian coopyright laws for  
#   modification.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
#   This program is designed to provide the interface to the MA, VAL and LOG
#   file generated for/by the CD++ simulation tool.
#   
#   This file is the file that is run as a script and will dynamically
#   import a selected file name contained within the *.blend file directory
#   
#   This file will create an reference to the class defined in the selected
#   file called MyClass. If the class is not present or renamed, this file will
#   fail to execute and generate errors.
#   
#   The file selection 'dropdown' or combobox for the MA, VAL, and LOG files
#   are dynamically generated and are regenerated each time the script is run
#   or when the script is moved to another directory.
#
#   IT IS ASSUMED THAT A VALID MA, VAL OR LOG FILE ARE PRESENT IN THE DIRECTORY
#   IF REQUIRED AND FAILURE AND EXCEPTIONS WILL BE GENERATED IF THESE MANDATORY 
#   FILES ARE NOT PRESENT. FAILURE TO OPEN A FILE WILL CAUSE BLENDER TO EXIT
#   NOT CRASH TO PROVIDE THE USER WITH A FILE OPENING PROBLEM.
# --------------------------------------------------------------------------

__author__ = "Colin Timmons"
__version__ = "0.1"
__bpydoc__ = """ CD++ Simulations Interface 0.1

This script is designed to provide interface for the CD++ Simulation software.
Utilizing the script, one can import the local files in the blend file directory
and parse the code. Linked into the module is another file called cdpp that
caontains the applicable function in the class that permits Blender to 
render the CD++ simulation.
"""

import bpy
import os
import logging

defaultPath =  os.path.dirname( bpy.data.filepath ) + "\\"
print(os.path.dirname(bpy.data.filepath))

# --------------------------------------------------------------------------
#   This function provides the logging capability. Upon instantiation the
#   function returns a logger member variable accessible through the Python
#   module. Python module error and exceptions are logged into a FCInterface_log.txt
#   file. Trace back error are also logged in the file for off-tim viewing.
#
#   Member instantiation
#   logger = CreateLogger
# --------------------------------------------------------------------------
def CreateLogger():
    logger = logging.getLogger('cdpp_log')
    hdlr = logging.FileHandler(bpy.context.scene['defaultPath']+"\\"+"FCInterface_log.txt",mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s' )
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger
# --------------------------------------------------------------------------
#   This function provides the ability to dynamically store variables into the 
#   scene. This allows the Python console to access the variables and their
#   respective values. 
#
#   Function calling
#   initSceneProperties(defaultPath, ma_file, log_file, py_file)
# --------------------------------------------------------------------------
def initSceneProperties(defaultPath, ma_file, log_file, py_file):
    bpy.types.Scene.MyMaString = bpy.props.StringProperty(name="String")
    bpy.context.scene['MyMaString'] = defaultPath+ma_file
    bpy.types.Scene.MyLogString = bpy.props.StringProperty(name="String")
    bpy.context.scene['MyLogString'] = defaultPath+log_file
    bpy.types.Scene.MyPyString = bpy.props.StringProperty(name="String")
    bpy.context.scene['MyPyString'] = defaultPath+py_file
    bpy.types.Scene.defaulthPath = bpy.props.StringProperty(name="String")
    bpy.context.scene['defaultPath'] = defaultPath 
    return
# --------------------------------------------------------------------------
#   This class is the main class of this Python module and contains the methods
#   for accessing the MA VAL and LOG files created for or generated by the CD++
#   Simulation Tool. THe class is instantiated from the main execute button
#   exexute method located near the end of this script
#
#   Class instantiation
#   cdpp_op = CdppFileControl
#   cdpp_op = CdppFileControl()
#   cdpp_op.read_ma(scn['MyMaString'], 'r')  
#   cdpp_op.read_log(scn['MyLogString'], 'r')  
# --------------------------------------------------------------------------   
class CdppFileControl():

    # --------------------------------------------------------------------------
    #   __init__
    #
    #   Class constructor
    #
    #   path, parameter = example variables accessible through the class
    # --------------------------------------------------------------------------
    def __init__(self, path="", parameter=""):
        self.path = path
        self.parameter = parameter
        #
        #   Import whatever file the user has selected as the python file
        #   This file articulates the interface between Blender and the CD++ log file
        #
        import imp
        cdpp = imp.load_source('module.name',bpy.context.scene['MyPyString'])
        
        #
        #   Instantiate the class to interface with Blender
        #
        self.MyClass = cdpp.MyClass()
        
    # --------------------------------------------------------------------------
    #   OpenFile
    #
    #   Modularity method to provide IO capabilities and exception handling
    #
    #   path        : absolute file path
    #   parameter   : file access permission
    # --------------------------------------------------------------------------
    def OpenFile(self, file, parameter):
        global logger
        operation = ""
        if (parameter == 'r'):
            logger.info("Opening readonly file "+file)
            operation = "read"
        else:
            logger,info("Opening writeable file "+file)
            operation = "write"
        try:
            return(open(file, parameter))
        except:
                logger.exception("Unable to open the file")
                print ("File opening failure. Exiting ...")
                logger.exception("Failure to open file: "+file+" as " + operation + "Exiting")
                
        return
        
    # --------------------------------------------------------------------------
    # read_ma(self, path, parameter='r')
    #
    # Read and parse CD++ ma file
    #   Currently only looks for the .val file to setup visual environment
    #
    # path : full path of the CD++ ma file
    # --------------------------------------------------------------------------
    def read_ma(self, path, parameter='r'):
        global logger
        # Log that the MA file is being read
        logger.info("Reading ma file "+path)
        # Open the file
        maFile = self.OpenFile(path, parameter)
        
        # Look for a .val file and default InitialValue
        for line in maFile.readlines():
            #Split each line in an array. Separation is determined by whitespaces
            words = line.split()
            
            # Make sure the file was read and there is actual data present
            if len(words)>0:
                # Keywords are expected to be first word of line
                # Check for an initial value
                if words[0]=="initialvalue":
                    # Transfer the value read to a variable
                    # and log the variable value in the log file
                    defaultValue = words[2]
                    logger.info("Reading initialValue("+defaultValue+")")
                # Check for a VAL file name. It is a file name without the path
                elif words[0]==("initialCellsValue"):
                    # Transfer the file name to a variable
                    # and log the file name with the path of the file
                    valfilename=defaultPath+words[2]
                    logger.info("Reading initialCellsValue file("+valfilename+")")
                    #Read the VAL file
                    self.read_val(valfilename, 'r')
        maFile.close()
        
    # --------------------------------------------------------------------------
    # read_val(self, path, parameter='r')
    #
    # Read and parse CD++ val file
    #   Setup initial values for visual environment
    #
    # path : full path of the CD++ val file
    # --------------------------------------------------------------------------
    def read_val(self, path, parameter='r'):
        global logger
        # Log that the VAL file is being read
        logger.info("Reading VAL file "+path)
        # Open the VAL file as read-only
        valFile = self.OpenFile( path, parameter)
        # Cycle through all the elines of the file
        for line in valFile.readlines():
            #Split each line in an array. Separation is determined by a '='
            words=line.split('=')
            # the size of value must be more than 2 
            if len(words)>=2:
                # Python returns a zero for a zero value
                # It also returns a zero for an error
                # Preset the time variable for the DCD Python class to be called later
                time="00:00:00"
                cell=words[0]
                logValueWorld=words[1]
                try:
                    # Call the main event method in the DCD Python module to populate based
                    # on the initial specifications
                    self.MyClass.apply_log(cell.strip(),time,logValueWorld.strip())
                except:
                    # Log that an exception happen and the logging function
                    # will automatically write the excepyion to the log file
                    logger.exception("Unable to process val file")
                    # The file was opened but unreadable. Close the file
                    valFile.close();
        valFile.close()
    
    # --------------------------------------------------------------------------
    # read_log(self, path)
    #
    # Read and parse CD++ log file
    #
    # path : full path of the CD++ log file
    # --------------------------------------------------------------------------
    def read_log(self, path, parameter='r'):
        global logger, cdpp
        # Log that the LOG file is being read
        logger.info("Reading log file "+path + " as readonly" )
        # Open the LOG file as read-only
        cdppLogFile = self.OpenFile(path, parameter)
        
        # Look for messages in the CD++ log file
        for line in cdppLogFile.readlines():
            #Split each line in an array. Separation is determined by whitespaces
            words = line.split()
            # Depending on the message delivered by the CD ++ Simulation Tool
            # One message format or more may be needed. THis could have been
            # joined but it is easier to trace back one messge type rather than
            # two at the same time.
            # Uncomment the X message format as required or add if another type of message is needed.
            # Make sure the statements line up i.e ctrl f to bring up the propertiy sheet
            # of this text editor. Click 'show margin' and a red line appears. Adjust the
            # margin column box to move the red line so that blocks are lined up.
            # The slashes in the log file are the even array cells when the
            # each line is read
            # For ac_eval only Y messages are processed
            if (len(words) > 1) and (words[1] == ("Y")):
                time          = words[3]
                srcName       = words[5]
                port          = words[7]
                logValueWorld = words[9]                
                destModel     = words[11]
                try:
                    # Attempt to populate the DCD Python module with the appropriate data information
                    self.MyClass.apply_log( srcName.strip(), time, logValueWorld.strip(), destModel.strip(), port.strip())
                except:
                    #Belief is in always having exception handler especially togive detail to the error
                    logger.exception("Error raised. Unable to parse cdpp log file: "+path+ " srcName was: "+srcName)
                    # The file was opened and parsed but there was an error raised in the DCD Python module
                    cdppLogFile.close()
        #   elif (len(words) > 1) and (words[1] == ("X")):
        #       time          = words[3]
        #       srcName       = words[5]
        #       port          = words[7]
        #       logValueWorld = words[9] 
        #       destModel     = words[11] 
        #       try:
        #           self.MyClass.apply_log( srcName.strip(), time, logValueWorld.strip(), destModel.strip(), port.strip())
        #       except:
        #           logger.exception("Error raised. Unable to parse cdpp log file: "+path+ " srcName was: "+srcName)
        #           cdppLogFile.close()
        # Successful reading of the Log file? Close the file anyhow.
        
        logger.info("Closing log file "+path )           
        cdppLogFile.close()
        
        #AC_Evac replicates cell and fills up memory so delete the cells after the modelling
        self.MyClass.deleteReplication('Cell')
        logger.info("Deleting replicated cells produced and left over " )
# --------------------------------------------------------------------------
# class DialogOperator()
#
# Creates pop-up window for CD++ file execution when the script is run
#
# baseclass bpy.types.Operator
# --------------------------------------------------------------------------
class DialogOperator(bpy.types.Operator):
    # Identifier
    bl_idname = "object.dialog_operator"
    # Popup menu heading
    bl_label = "CD++ Simulation Interface"
    
    #
    #   Local class declaration field
    #
    extma  = "ma"
    extlog = "log"
    extpy  = "py"
    extObj = "."
    ma_counter  = 0
    log_counter = 0
    py_counter  = 0
    fileMaList  = []
    fileLogList = []
    filePyList  = []
    defaultMaFile    = ""
    defaultLogFile   = ""
    defaultSceneFile = ""
    
    defaultPath = os.path.dirname( bpy.data.filepath )
    defaultPath += "\\"
    
    
    #
    #   Search through the current directory and locate ma, log, and py files.
    #   Populate the drop down list with the first found.
    #   Do not populate the Python file list with this file
    #    
    for index, file in  enumerate( os.listdir( os.path.dirname( bpy.data.filepath ) ) ):
        if file[-len(extma):] == extma:
            fileMaList.append((str(ma_counter),file,file))
            ma_counter = ma_counter + 1
            ma_file_selected = bpy.props.EnumProperty(items=fileMaList, default='0')
            
        elif file[-len(extlog):] == extlog:            
            fileLogList.append((str(log_counter),file,file))
            log_counter = log_counter + 1
            log_file_selected = bpy.props.EnumProperty(items=fileLogList, default='0')
            
        elif file[-len(extpy):] == extpy:
            if file == "file_control.py":
                continue
            filePyList.append((str(py_counter),file,file))
            py_counter = py_counter + 1
            py_file_selected = bpy.props.EnumProperty(items=filePyList, default='0')
            
           
    # --------------------------------------------------------------------------
    # draw(self,context)
    #
    # Overridden method to populate the pop-menu 
    # --------------------------------------------------------------------------                                  
    def draw(self,context):
        #
        #   Accept the base class window as the default
        #
        layout = self.layout
        
        #
        #   Each line of code is for the format of the popmenu and is self explanatory 
        #
        layout.separator()
        # Shown the blend file
        # With Blender if the "save as default' command button is used it appears that
        # there is a Blend file loaded. However, this is not so. The student could be
        # working seeing a  blend file output window in the 3D view area but actually
        # no Blend file is loaded. This gives a visual acuity of the state of Blender 
        layout.label(context.scene.name + ": " + bpy.data.filepath)
        layout.separator()
        #Create the combo boxes and diapplay them.
        # The value of the selectionis stored in the <self.StringName> as shown in the quotes
        layout.prop(self, "ma_file_selected", text="Default MA Files")   #draw MA dropdown box on panel with text field
        layout.prop(self, "log_file_selected", text="default LOG Files") #draw LOG dropdown box on panel with text field
        layout.prop(self, "py_file_selected", text="Default PY Files")   #draw PY dropdown box on panel with text field
        layout.separator()
        
        #
        #   Place the exe command button on the popup menu
        #
        layout.operator("exe.button")
        
    # --------------------------------------------------------------------------
    # execute(self,context)
    #
    # Overridden method for execute of the pop-menu 
    # --------------------------------------------------------------------------  
    def execute(self, context):
        #
        #   Log information on what files are being used
        #
        logger.info("Parsing MA file: " + defaultMaFile)
        logger.info("Parsing CD++ log file: " + defaultLogFile)
        logger.info("Using blend file: " + bpy.data.filepath) 
        logger.info("\n")  
        logger.info("*****************************")
        logger.info("* End of logging sequence   *")
        logger.info("*****************************")
        return {'FINISHED'}

    # --------------------------------------------------------------------------
    # invoke(self,context)
    #
    # Overridden method for initial creation of the dialog 
    # --------------------------------------------------------------------------  
    def invoke(self, context, event):
                  
        if event.type == 'ESC':
            return {'CANCELLED'}


        #
        #   Set simple variables to pass to the execution method
        #   The -1 value for display however defaults in python to the end of the array
        #
        try:
            defaultMaFile = self.fileMaList[(int)(self.ma_file_selected)][2]
            defaultLogFile = self.fileLogList[(int)(self.log_file_selected)][2]
            defaultPyFile = self.filePyList[(int)(self.py_file_selected)][2]
            
            #
            #   Dynamically store the files into the scene for access by other classes
            #
            initSceneProperties(self.defaultPath, defaultMaFile, defaultLogFile, defaultPyFile)
            
            #
            #   When invoked set the size of the pop window
            #
            wm = context.window_manager
            return wm.invoke_props_dialog(self, width = 200)
        except:
            print("Unable to open the current directory for either a MA, LOG or PYTHON file")       
            #bpy.ops.wm.quit_blender()
            return {'CANCELLED'}

        
       
        

# --------------------------------------------------------------------------
# class for custom execute button
#
# base class - bpy.types.Operator
# --------------------------------------------------------------------------
class CustomExeButton(bpy.types.Operator):
    bl_idname = "exe.button"
    bl_label = "Execute Simulation"
    
    
    
    # --------------------------------------------------------------------------
    # execute(self,context)
    #
    # Overridden method for execute of the execute command button
    # --------------------------------------------------------------------------
    def execute(self, context):
        scn = context.scene
        
        
        #
        #   Upon command to execute the reading of the files, call the 'reading' file class
        #
        cdpp_op = CdppFileControl()
        cdpp_op.read_ma(scn['MyMaString'], 'r')  
        cdpp_op.read_log(scn['MyLogString'], 'r')       
        return{'FINISHED'} 

# --------------------------------------------------------------------------
# register()
#
# Function to register the derived classes to let the system know they are available
# --------------------------------------------------------------------------
def register():
    bpy.utils.register_class(DialogOperator)
    bpy.utils.register_class(CustomExeButton)
    
# --------------------------------------------------------------------------
# unregister()
#
# Function to unregister the derived classes to let the system know they are no longer available
# --------------------------------------------------------------------------
def unregister():
    bpy.utils.unregister_class(DialogOperator)
    bpy.utils.unregister_class(CustomExeButton)
    
# --------------------------------------------------------------------------
# main loop()
#
# Function to get the program to run
# --------------------------------------------------------------------------
if __name__ == "__main__":
    #
    #   Register the classes
    #
    register()
    
    #
    #   Invoke the popup menu dialog
    #
    ret = bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
    print("ret = : ",ret)
    if ret != {'CANCELLED'}:
        #
        #   Create a logging file for this python script
        #   
        logger = CreateLogger()
        
        #
        #   Log that the simulation is commencing
        #
        logger.info("*****************************")
        logger.info("* Start of logging sequence *")
        logger.info("*****************************")
        logger.info("\n")
        logger.info("Executing CD++/Blender Simulation Visualisation Tool...")
        logger.info("\n")
        
       
    
