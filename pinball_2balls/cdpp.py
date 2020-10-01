bl_info = {
    "name": "PIN Ball simulation",
    "author": "Prasanthi and Yamini",
    "version": (0,1),
    "blender": (2, 60, 0),
    "api": 41226,
    "location": "Ottawa, Ontario",
    "description": "Simulates the aircraft evacuation based on cellular automata data log",
    "warning": "",
    "wiki_url":""
    }

###########################################################################
#   Copyright (C) 2011 Colin Timmons
#
#   This program is free software developed in house for SYSC 5104
#   Discrete Modelling and Simulation at Carletob University.
#
#   This program is free to distribute and or modify under the
#    terms of the applicable contract copyright laws for distribution
#   of the present country and undre Canadian coopyright laws for
#   modification.
#
# Based on the original modelling technique of Emil Poliakov Blender 2.41- Dec 2007
# Modified by Kin Wing Tsui - Dec 2007
# Modified by Patrick Castonguay - 4 Sept 2008
###########################################################################

__bpydoc__ = """	CD++ Simulations Auto Factory 0.1
    This script is designed to animate for the CD++ Simulation software.
    Utilizing the script, one can animate the scene based on the import of
    the current directory log file output for CD++."""
import bpy
import os
import logging
import time
import logging


# --------------------------------------------------------------------------
# CreateLogger()
#
# Enables logging to MyClass.log
# --------------------------------------------------------------------------
def CreateLogger():
    defaultPath = os.path.dirname( bpy.data.filepath )
	
    defaultPath += "\\" 
    logger = logging.getLogger('MyClass')
    hdlr = logging.FileHandler(defaultPath+"\\"+"MyClass.log",mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s' )
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger

# --------------------------------------------------------------------------
# returnObjectByName(passedName= "")
#
# Reinvented function for the get function lost since version 2.49
#
# passedName: name to call the cell
# --------------------------------------------------------------------------
def returnObjectByName(passedName= ""):
    obj_name = None
    obs = bpy.data.objects
    for ob in obs:
        if ob.name == passedName:
            obj_name = ob
    return obj_name
    
    
# --------------------------------------------------------------------------
# SelectAndDuplicate(cell, name)
#
# Common function to 
#
# cell :        cell to handle 
# time :        timestamp of the message
# valueWord :   string containing the numeric value in the message
# --------------------------------------------------------------------------
def SelectAndDuplicate(cell, name):
    global myClasslog
    bpy.ops.object.select_all(action='DESELECT')
    myClasslog.info("The desired name of the new duplicated object is : "+ name)
    if name != "":
        scn = bpy.data.scenes['Scene']
        bpy.ops.object.select_name(name=cell)
        new_obj = bpy.ops.object.duplicate_move()
        bpy.context.object.name = name
        myClasslog.info("The name of the new duplicated object is : "+ bpy.context.object.name)
        
        new_obj = bpy.context.scene.objects.active
        return new_obj
# 
#   Create a member variable to log results to file
# 
myClasslog = CreateLogger()

class MyClass():
    
    def __init__(self, cell="", myTime="", logValueWord=""):
        self.cell = cell
        self.myTime = myTime
        self.logValueWord = logValueWord
        
          
        myClasslog.info("***************************")
        myClasslog.info(" MyClass initiated         ")
        myClasslog.info("***************************")

        self.group = self.createGrp('cells')
    # --------------------------------------------------
    # convertStr(self,myString )
    #
    # returns either a float or int value of a string
    #
    # value:  the string being passed
    # --------------------------------------------------
    def convertStr(self, myString):
        #
        #  Convert string to either int or float.
        #
        try:
            ret = int(myString)
        except ValueError:
            #Try float.
            ret = float(myString)
        return ret
    
       
    # --------------------------------------------------
    # createGrp(self, grpName)
    #
    # Creates a grouping for objects
    #
    # string grpName    : group name
    # --------------------------------------------------
    def createGrp(self, grpName):
        group_name = None
        if not grpName in bpy.data.groups:
            bpy.ops.group.create(name=grpName)
        return( bpy.data.groups[grpName] )
            
        myClasslog.info("Group "+ grpName +" created")
            
        
    # --------------------------------------------------
    # deleteGroup(self, grpName)
    #
    # Deletes a grouping for objects
    #
    # string grpName    : group name
    # --------------------------------------------------
    def deleteGrp(self, grpName):
        group_name = bpy.data.groups.get(grpName)
        
        if group_name in list(bpy.data.groups):
            bpy.data.group.remove(group_name)
            myClasslog.info("Group "+ grpName +" deleted")
            
    # --------------------------------------------------
    # linkGroupObjs(self, name, grpName)
    #
    # Link objects into groups
    #
    # string name       : object name
    # string grpName    : group name
    # --------------------------------------------------
    def linkGrpObjs(self, name, grpName):
        group_name = None
        obj = None

        if grpName in bpy.data.groups:
            group_name = bpy.data.groups[grpName]
        else:
            self.createGrp(grpName)
            group_name = bpy.data.groups[grpName]
        
        if name in bpy.data.objects:
            obj = bpy.data.objects[name]
            
        if not obj.name in group_name.objects:
            group_name.objects.link(obj)
            myClasslog.info("Object "+ obj.name +" linked into group :" + group_name.name)
            
    # --------------------------------------------------
    # unlinkGroupObjs(self, name, grpName)
    #
    # Unlink objects from groups
    #
    # string name       : object name
    # string grpName    : group name
    # --------------------------------------------------
    def unlinkGrpObjs(self, name, grpName):
        group_name = None
        obj = None
        
        obj = returnObjectByName(name)
        if grpName in bpy.data.groups:
            group_name = bpy.data.groups[grpName]
        
        if name in bpy.data.objects:
            obj = bpy.data.objects[name]
            
        if obj.name in group_name.objects:
            group_name.objects.unlink(obj)
            myClasslog.info("Object "+ obj.name +" unlinked from group :" + group_name.name)
     
    # --------------------------------------------------
    # deleteObj(self, name)
    #
    # Deletes an object from existence
    #
    # string name    : object name
    # --------------------------------------------------
    def deleteObj(self, name):
         obj = None
         if name in bpy.data.objects:
            obj = bpy.data.objects[name]
         if obj:
            #Delink them first from the scene
            bpy.context.scene.objects.unlink(obj)
            myClasslog.info("Object "+ name +" unlinked")
            obj.user_clear() 
            bpy.data.objects.remove(obj)
  
            myClasslog.info("Object "+ name +" deleted")
  
         
    # --------------------------------------------------
    # deleteReplication(self, name)
    #
    # Deletes all specified by name objects 
    #
    # string name    : object wildcard name
    # --------------------------------------------------
    def deleteReplication(self, name):
        wildcard = name+'*'
        # This sets all objects matching the pattern
        bpy.ops.object.select_pattern(pattern=wildcard)
        #Create a list of the selected items
        objList = bpy.context.selected_objects
        for obj in objList:
            self.deleteObj(obj.name)
            
    #-------------------------------------------------------------------------
    # apply_log(self, cell, myTime, logValueWord)
    #
    # Interpret CD++ log file data for Blender animation
    #
    # cell :        cell to handle 
    # time :        timestamp of the message
    # valueWord :   string containing the numeric value in the message
    # --------------------------------------------------------------------------
    def apply_log(self, cell, myTime, logValueWorld, destModel="", port=""):
        global myClasslog, activeObject
               
        myClasslog.info("Simulation time: "+str(myTime)+", Processing "+str(cell)+" with value "+str(logValueWorld) )
        
        # Time expected to be CD++ kind 00:00:00:000; transform it for Blender
        # It is used as a frame setup.  For ac_evac the increment used is seconds
        #Ignore microseconds
        myTime = myTime[0:8]
        
        pattern = '%H:%M:%S'
        epoch =  time.strptime(myTime, pattern)  
        totalTime = int((epoch[3] * 60 + epoch[4]) * 60.0 + epoch[5])
        
        bpy.context.scene.frame_set(totalTime)
                
        scn = bpy.data.scenes["Scene"]
        
        # Get cell description currently works for three dimensions
        # cells are always described as 'modelName'(x,y)(..)
        # zeroize position counters to be more versatile than previous version
        a = b = c = d = 0
        for i in range(len(cell)):
            if cell[i]=='(' and cell[i-1]!=')':
                a = i
            elif cell[i]==',' and b==0:
                b = i
            elif cell[i]==')' and c==0:
                c = i
            
                
        #Transform description into coordinates
        xcoord = (cell[a+1:(a+len(range(a,b)))])
        ycoord = (cell[b+1:(b+len(range(b,c)))])
        
        
        #Only first plane is used in ac_evac simulation to represent movement
        #the other is used for background calculation within the CD++ model
        
        #Exit the function apply_log
        
        logValue = self.convertStr(logValueWorld)
        # Set object name to the 

		#cell
        objectname = ("Cell_"+xcoord+"_"+ycoord)
		
        myClasslog.info("Processing: "+objectname)
        scene_obs = list(bpy.data.objects)
        try:
            # Process state values that are passed as logValue for the current cell
            if ((logValue == 1) or (logValue == 2) or (logValue == 3) or (logValue == 4) or (logValue == 5) or (logValue == 6) or (logValue == 7) or (logValue == 8)):
                # Occupied cell (ball)
                
                ob = returnObjectByName(objectname)
                if not ob:
                    myClasslog.info("Cell was not present and was linked in for display")
					#myClasslog.info("cell value is", logValue)
                    myClasslog.info("Sphere not found in scene ... adding to scene")
                    activeObject = SelectAndDuplicate('Sphere', objectname)
                    self.linkGrpObjs(objectname,self.group.name)
                    myClasslog.info("Sphere set to xy coord "+ xcoord+ycoord)
                    activeObject.location.xy = [int(xcoord), int(ycoord)]
                    #myClasslog.info("Human checking direction") 
                    # if (activeObject.location==19 and activeObject.location<=5):
                        # activeObject.rotation_euler[2]=4.71
                        # activeObject.location.y+=1
                        # myClasslog.info("Object Human rotated 270 degrees in aft stbd plane ")
                    # elif (activeObject.location.y==19 and activeObject.location.x>5):
                        # activeObject.rotation_euler[2]=1.57
                        # activeObject.location.x+=1
                        # myClasslog.info("Object Human rotated 90 degrees in aft port plane")
                    # elif (activeObject.location.y>=10 and activeObject.location.y!=19 and (activeObject.location.x==8 or activeObject.location.x==3)):
                        # activeObject.rotation_euler[2]=3.14
                        # activeObject.location.x+=1
                        # myClasslog.info("Object Human rotated 180 degrees for aft plane in aisle ")
                    # elif (activeObject.location.y==1 and activeObject.location.x<=5):
                        # activeObject.rotation_euler[2]=4.71
                        # activeObject.location.y+=1
                        # activeObject.location.y-=1  
                        # myClasslog.info("Object Human rotated 270 degrees in forward stbd plane ")
                    # elif (activeObject.location.y==1 and activeObject.location.x>5):
                        # activeObject.rotation_euler[2]=1.57
                        # activeObject.location.x+=1
                        # myClasslog.info("Object Human rotated 90 degrees in forward port plane ")
                    bpy.ops.object.select_all(action='DESELECT')
                    myClasslog.info("Object Sphere created ")

            elif (logValue == 9): # Wall or obstacle
                try:
				    
                    activeObject = SelectAndDuplicate('Cube', objectname)
                    self.linkGrpObjs(objectname,self.group.name)
                    activeObject.location.xy = [int(xcoord), int(ycoord)]
                    
                    myClasslog.info("Object cube created")
                except ValueError:
				    
                    myClasslog.info("Object cube already exist or error occured**\n")
            # elif (logValue == -9): # Chair
                # try:
                    # activeObject = SelectAndDuplicate('Chair', objectname)
                    # self.linkGrpObjs(objectname,self.group.name)
                    # activeObject.location.xyz = [int(xcoord), int(ycoord), int(zcoord)]
                   
                    # myClasslog.info("Object chair created")
                # except ValueError:
                    # myClasslog.error("Object chair already exist or error occured")
            # elif (logValue == 9): # Emergency exit
                # try:
                    # activeObject = SelectAndDuplicate('Cube.Exit', objectname)
                    # self.linkGrpObjs(objectname,self.group.name)
                    # activeObject.location.xyz = [int(xcoord), int(ycoord), int(zcoord)]  
                    # myClasslog.info("Emergency exit created")
                # except ValueError:
                    # myClasslog.error("Object cube already exist or error occurred")
            elif (logValue == 0): # Empty cell
                try:
                    #works great now to remove it
                    #bpy.context.scene.objects.unlink(bpy.data.objects[objectname])
                    
                    ob = returnObjectByName(objectname)
                    if ob:
                        obj = bpy.data.objects[objectname]
                        bpy.context.scene.objects.unlink(obj)
                        obj.user_clear() # If don't use this function, some object cannot delete and raise error.
                        bpy.data.objects.remove(obj)
                        myClasslog.info("Object "+ ob.name +" unlinked")
                except:
                    myClasslog.info("Object "+ ob.name +" not able to be unlinked")
            else:
                myClasslog.error("Log value not recognised as valid: %d" %(logValue))
        except ValueError:
            myClasslog.critical("\n")
            myClasslog.critical("*****************************************")
            myClasslog.critical("* Unexpected stop to logging sequence   *")
            myClasslog.critical("*   in apply_log() portion of script    *")
            myClasslog.critical("*****************************************")
        # Refresh the display
        scn.update()
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
   

        
       
