# -*- coding: utf-8 -*-
"""

This is a Calculator class that returns various statistics about given data
"""

import math

class Calculator:
    """
    A class that returns various statistics about given data.
    
    
    Attributes
    ----------
    data : list
        The data set
    mean : int, float
        The mean of the data set
    median : int, float
        The median of the data set
    variance : float
        The variance of the data set
    standev : float
        The standard deviation of the data set
        
    """
    def __init__(self,data):
        """
        Accepts a list of numbers as the argument.
        
        Parameters
        ----------
        data : list[int,float]
            A list of numbers that we want information about
            
        """
        assert all(isinstance(x,(int, float)) for x in data), "Data can only be numbers."
        assert len(data) > 1, "Data must be at least 2 numbers."
        self.data = data
        self.__update()
#         self.__length = len(self.data)
#         self.mean = self.__calc_mean()
#         self.median = self.__calc_median()
#         self.variance = self.__calc_var()
#         self.standev = self.__calc_stdv()

# Updates the statistics of the current data
    def __update(self):
        """Updates the length, mean, median, variance, and standard deviation of the data."""
        self.length = len(self.data)
        self.mean = self.__calc_mean()
        self.median = self.__calc_median()
        self.variance = self.__calc_var()
        self.standev = self.__calc_stdv()

    def __calc_mean(self):
        mean = sum(self.data)/self.length
        return mean
    
    def __calc_median(self):
        srt_data = sorted(self.data)
        if self.length%2 == 0:
            median = (srt_data[self.length//2 - 1]+srt_data[self.length//2])/2
        else:
            median = srt_data[self.length//2]
        return median
    
    def __calc_var(self):
        return sum([(x-self.mean)**2 for x in self.data])/(len(self.data)-1)
    
    def __calc_stdv(self):
        return math.sqrt(self.variance)
 
# Adds new data to our existing data. Can accept single elements or list of
# new elements. Calls update after the data is changed.
    def add_data(self,new_data):
        """
        Adds new data into the data set.
        
        Parameters
        ----------
        new_data : int, float, list[int, float]
            Either a single number or a list of numbers to be added to the
            data set.
            
        """
        if type(new_data)==list:
            assert all(isinstance(x,(int, float)) for x in new_data), "Data can only be numbers"
            self.data.extend(new_data)
        else:
            assert isinstance(new_data, (int, float)), "Data can only be numbers"
            self.data.append(new_data)
        self.__update()
        
# Removes an element at the specified index from data. Calls update after the
# data is changed.
    def remove_data(self,index):
        """
        Removes the number at the given index from the data set.
        
        Parameters
        ----------
        index : int
            The index of the number that you want removed.
        
        """
        assert index < len(self.data), "Index out of bounds. Data only has "+str(len(self.data))+" elements."
        assert len(self.data) > 3, "Cannot delete anymore data. Data must have at least 2 numbers."
        del self.data[index]
        self.__update()
        
    
# new_calc = Calculator([55, 56, 56, 58, 60, 61, 63, 64, 70])