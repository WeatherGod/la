"""Unit tests of sector module."""

import unittest

import numpy as np
import numpy.matlib as M
np.seterr(divide='ignore')
np.seterr(invalid='ignore')
nan = np.nan

from test import printfail
from la.afunc import sector_rank, sector_mean, sector_median
from la.afunc import (movingsum, ranking_1N, movingrank, ranking_norm,
                      movingsum_forward, geometric_mean, ranking, unique_sector,
                      sector_dummy)

# Sector functions ----------------------------------------------------------

class Test_sector_rank(unittest.TestCase):
    """Test afunc.sector_rank"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8
        self.x = np.array([[0.0, 3.0, nan, nan, 0.0, nan],
                           [1.0, 1.0, 1.0, nan, nan, nan],
                           [2.0, 2.0, 0.0, nan, 1.0, nan],
                           [3.0, 0.0, 2.0, nan, nan, nan],
                           [4.0, 4.0, 3.0, 0.0, 2.0, nan],
                           [5.0, 5.0, 4.0, 4.0, nan, nan]])
        
    def test_sector_rank_1(self):
        "afunc.sector_rank #1"
        sectors = ['a', 'b', 'a', 'b', 'a', 'c']
        theory = np.array([[-1.0, 0.0,  nan, nan, -1.0, nan],
                           [-1.0, 1.0, -1.0, nan,  nan, nan],
                           [ 0.0,-1.0, -1.0, nan,  0.0, nan],
                           [ 1.0,-1.0,  1.0, nan,  nan, nan],
                           [ 1.0, 1.0,  1.0, 0.0,  1.0, nan],
                           [ 0.0, 0.0,  0.0, 0.0,  nan, nan]])
        practice = sector_rank(self.x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_sector_rank_2(self):
        "afunc.sector_rank #2"
        sectors = ['a', 'b', 'a', 'b', 'a', None]
        theory = np.array([[-1.0,  0.0,  nan, nan,-1.0, nan],
                           [-1.0,  1.0, -1.0, nan, nan, nan],
                           [ 0.0, -1.0, -1.0, nan, 0.0, nan],
                           [ 1.0, -1.0,  1.0, nan, nan, nan],
                           [ 1.0,  1.0,  1.0, 0.0, 1.0, nan],
                           [ nan,  nan,  nan, nan, nan, nan]])
        practice = sector_rank(self.x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)                                          

class Test_sector_mean(unittest.TestCase):
    """Test afunc.sector_mean"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8
        self.x = np.array([[0.0, 3.0, nan, nan, 0.0, nan],
                           [1.0, 1.0, 1.0, nan, nan, nan],
                           [2.0, 2.0, 0.0, nan, 1.0, nan],
                           [3.0, 0.0, 2.0, nan, nan, nan],
                           [4.0, 4.0, 3.0, 0.0, 2.0, nan],
                           [5.0, 5.0, 4.0, 4.0, nan, nan]])
        
    def test_sector_mean_1(self):
        "afunc.sector_mean #1"
        sectors = ['a', 'b', 'a', 'b', 'a', 'c']
        theory = np.array([[ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 5.0, 5.0,  4.0, 4.0,  nan, nan]])
        practice = sector_mean(self.x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_sector_mean_2(self):
        "afunc.sector_mean #2"
        sectors = ['a', 'b', 'a', 'b', 'a', None]
        theory = np.array([[ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ nan, nan,  nan, nan,  nan, nan]])
        practice = sector_mean(self.x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)

    def test_sector_mean_3(self):
        "afunc.sector_mean #3"
        sectors = ['a', 'b', 'a', 'b', 'a']
        x = np.array([[1,2],
                      [3,4],
                      [6,7],
                      [0,0],
                      [8,-1]])
        theory = np.array([[5.0,8/3.0],
                           [1.5,2.0],
                           [5.0,8/3.0],
                           [1.5,2.0],
                           [5.0,8/3.0]])
        practice = sector_mean(x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)            

class Test_sector_median(unittest.TestCase):
    """Test afunc.sector_median"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8
        self.x = np.array([[0.0, 3.0, nan, nan, 0.0, nan],
                           [1.0, 1.0, 1.0, nan, nan, nan],
                           [2.0, 2.0, 0.0, nan, 1.0, nan],
                           [3.0, 0.0, 2.0, nan, nan, nan],
                           [4.0, 4.0, 3.0, 0.0, 2.0, nan],
                           [5.0, 5.0, 4.0, 4.0, nan, nan]])
        
    def test_median_1(self):
        "afunc.sector_median #1"
        sectors = ['a', 'b', 'a', 'b', 'a', 'c']
        theory = np.array([[ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 5.0, 5.0,  4.0, 4.0,  nan, nan]])
        practice = sector_median(self.x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_sector_median_2(self):
        "afunc.sector_median #2"
        sectors = ['a', 'b', 'a', 'b', 'a', None]
        theory = np.array([[ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ 2.0, 0.5,  1.5, nan,  nan, nan],
                           [ 2.0, 3.0,  1.5, 0.0,  1.0, nan],
                           [ nan, nan,  nan, nan,  nan, nan]])
        practice = sector_median(self.x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)

    def test_sector_median_3(self):
        "afunc.sector_median #3"
        sectors = ['a', 'b', 'a', 'b', 'a']
        x = np.array([[1,2],
                      [3,4],
                      [6,7],
                      [0,0],
                      [8,-1]])
        theory = np.array([[6.0,2.0],
                           [1.5,2.0],
                           [6.0,2.0],
                           [1.5,2.0],
                           [6.0,2.0]])
        practice = sector_median(x, sectors)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)


class Test_sector_oth(unittest.TestCase):
    """Test afunc.sector_mean"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8
                
    def test_sector_dummy_1(self):
        "afunc.sector_dummy #1"
        sectors = ['a', 'b', 'a', 'b', 'a', 'c']
        theory1 = np.matrix([[ 1.,  0.,  0.],
                            [ 0.,  1.,  0.],
                            [ 1.,  0.,  0.],
                            [ 0.,  1.,  0.],
                            [ 1.,  0.,  0.],
                            [ 0.,  0.,  1.]])
        theory2 = ['a', 'b', 'c']
        theory = (theory1, theory2)
        practice = sector_dummy(sectors)
        msg = printfail(theory, practice)
        theory1[np.isnan(theory1)] = self.nancode
        practice[0][np.isnan(practice[0])] = self.nancode        
        self.assert_(np.all(theory[0] == practice[0]), msg) 
        self.assert_(theory[1] == practice[1], msg) 
        
    def test_sector_unique_1(self):
        "afunc.unique_sector #1"
        sectors = ['a', 'b', 'a', 'b', 'a', 'c']
        theory = ['a', 'b', 'c']
        practice = unique_sector(sectors)
        msg = printfail(theory, practice)
        #theory[np.isnan(theory)] = self.nancode
        #practice[np.isnan(practice)] = self.nancode        
        self.assert_(theory == practice, msg)      

    
# Normalize functions -------------------------------------------------------

class Test_ranking_1N(unittest.TestCase):
    """Test afunc.ranking_1N"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8

    def test_ranking_1N_1(self):
        """afunc.ranking_1N #1"""
        x = np.array([[ 1.0, nan, 2.0, nan, nan],
                      [ 2.0, 2.0, nan, nan, nan],
                      [ 3.0, 3.0, 3.0, 3.0, nan]])
        theory = np.array([[ 0.0, nan, 0.0, nan, nan],
                           [ 1.0, 0.0, nan, nan, nan],
                           [ 2.0, 2.0, 2.0, 1.0, nan]])                     
        practice = ranking_1N(x, axis=0)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_ranking_1N_2(self):
        """afunc.ranking_1N #2"""
        x = np.array([[ 1.0, nan, 2.0, nan, nan],
                      [ 2.0, 2.0, nan, nan, nan],
                      [ 3.0, 3.0, 3.0, 3.0, nan]])
        theory = np.array([[ 0.0, nan, 0.0, nan, nan],
                           [ 1.0, 0.0, nan, nan, nan],
                           [ 2.0, 2.0, 2.0, 1.0, nan]])                     
        practice = ranking_1N(x)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_ranking_1N_3(self):
        """afunc.ranking_1N #3"""
        x = np.array([[ 1.0, nan, 2.0, nan, nan],
                      [ 2.0, 2.0, nan, nan, nan],
                      [ 3.0, 3.0, 3.0, 3.0, nan],
                      [ 4.0, 2.0, 3.0, 1.0, 0.0]])   
        theory = np.array([[ 0.0,   nan,   4.0, nan, nan],
                           [ 0.0,   4.0,   nan, nan, nan],
                           [ 0.0, 4/3.0, 8/3.0, 4.0, nan],
                           [ 4.0,   2.0,   3.0, 1.0, 0.0]])                     
        practice = ranking_1N(x, axis=1)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_ranking_1N_4(self):
        """afunc.ranking_1N #4""" 
        x = np.array([3.0, 1.0, 2.0])[:,None]
        theory = np.array([2, 0, 1])[:,None]
        practice = ranking_1N(x, axis=0)
        msg = printfail(theory, practice)    
        self.assert_((theory == practice).all(), msg) 

    def test_ranking_1N_5(self):
        """afunc.ranking_1N #5"""  
        x = np.array([3.0, 1.0, 2.0])[:,None]
        theory = np.array([0, 0, 0])[:,None]
        practice = ranking_1N(x, axis=1)
        msg = printfail(theory, practice)    
        self.assert_((theory == practice).all(), msg)        

class Test_ranking_norm(unittest.TestCase):
    """Test afunc.ranking_norm"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8    

    def test_ranking_norm_1(self):
        """afunc.ranking_norm #1"""
        x = np.array([[ 1.0,   nan,   2.0,   nan,   nan],
                      [ 2.0,   2.0,   nan,   nan,   nan],
                      [ 3.0,   3.0,   3.0,   3.0,   nan]])
        theory = np.array([[-1.0,   nan,  -1.0,   nan,   nan],
                           [ 0.0,  -1.0,   nan,   nan,   nan],
                           [ 1.0,   1.0,   1.0,   0.0,   nan]])                     
        practice = ranking_norm(x, axis=0)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_ranking_norm_2(self):
        """afunc.ranking_norm #2"""
        x = np.array([[ 1.0,   nan,   2.0,   nan,   nan],
                      [ 2.0,   2.0,   nan,   nan,   nan],
                      [ 3.0,   3.0,   3.0,   3.0,   nan]])
        theory = np.array([[-1.0,   nan,  -1.0,   nan,   nan],
                           [ 0.0,  -1.0,   nan,   nan,   nan],
                           [ 1.0,   1.0,   1.0,   0.0,   nan]])                    
        practice = ranking_norm(x)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_ranking_norm_3(self):
        """afunc.ranking_norm #3"""
        x = np.array([[ 1.0,   nan,   2.0,   nan,   nan],
                      [ 2.0,   2.0,   nan,   nan,   nan],
                      [ 3.0,   3.0,   3.0, 3.0  ,   nan],
                      [ 4.0,   2.0,   3.0, 1.0  , 0.0  ]])   
        theory = np.array([[-1.0,   nan,   1.0,   nan,   nan],
                           [-1.0,   1.0,   nan,   nan,   nan],
                           [-1.0,-1/3.0, 1/3.0,   1.0,   nan],
                           [ 1.0,   0.0,   0.5,  -0.5,  -1.0]])                     
        practice = ranking_norm(x, axis=1)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_ranking_norm_4(self):
        """afunc.ranking_norm #4"""  
        x = np.array([3.0, 1.0, 2.0])[:,None]
        theory = np.array([1.0,-1.0, 0.0])[:,None]
        practice = ranking_norm(x, axis=0)
        msg = printfail(theory, practice)    
        self.assert_((theory == practice).all(), msg) 

    def test_ranking_norm_5(self):
        """afunc.ranking_norm #5"""  
        x = np.array([3.0, 1.0, 2.0])[:,None]
        theory = np.array([0.0, 0.0, 0.0])[:,None]
        practice = ranking_norm(x, axis=1)
        msg = printfail(theory, practice)    
        self.assert_((theory == practice).all(), msg)

class Test_ranking(unittest.TestCase):
    """Test afunc.ranking"""
    
    def setUp(self):
        self.nancode = -9999
        self.tol = 1e-8    

    def test_ranking_1(self):
        """afunc.ranking #1"""
        x = np.array([[ 1.0,   nan,   2.0,   nan,   nan],
                      [ 2.0,   2.0,   nan,   nan,   nan],
                      [ 3.0,   3.0,   3.0, 3.0  ,   nan]])
        theory = np.array([[-1.0,   nan,  -1.0,   nan,   nan],
                           [ 0.0,  -1.0,   nan,   nan,   nan],
                           [ 1.0,   1.0,   1.0,   0.0,   nan]])                     
        practice = ranking(x, axis=0)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_ranking_2(self):
        """afunc.ranking #2"""
        x = np.array([[ 1.0,   nan,   2.0,   nan,   nan],
                      [ 2.0,   2.0,   nan,   nan,   nan],
                      [ 3.0,   3.0,   3.0,   3.0,   nan]])
        theory = np.array([[-1.0,   nan,  -1.0,   nan,   nan],
                           [ 0.0,  -1.0,   nan,   nan,   nan],
                           [ 1.0,   1.0,   1.0,   0.0,   nan]])                    
        practice = ranking(x)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_ranking_3(self):
        """afunc.ranking #3"""
        x = np.array([[ 1.0,   nan,   2.0,   nan,   nan],
                      [ 2.0,   2.0,   nan,   nan,   nan],
                      [ 3.0,   3.0,   3.0, 3.0  ,   nan],
                      [ 4.0,   2.0,   3.0, 1.0  , 0.0  ]])   
        theory = np.array([[-1.0,   nan,   1.0,   nan,   nan],
                           [ 0.0,   0.0,   nan,   nan,   nan],
                           [ 0.0,   0.0,   0.0,   0.0,   nan],
                           [ 1.0,   0.0,   0.5,  -0.5,  -1.0]])                    
        practice = ranking(x, axis=1)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_ranking_4(self):
        """afunc.ranking #4"""  
        x = np.array([3.0, 1.0, 2.0])[:,None]
        theory = np.array([1.0,-1.0, 0.0])[:,None]
        practice = ranking(x, axis=0)
        msg = printfail(theory, practice)    
        self.assert_((theory == practice).all(), msg) 

    def test_ranking_5(self):
        """afunc.ranking #5"""  
        x = np.array([3.0, 1.0, 2.0])[:,None]
        theory = np.array([0.0, 0.0, 0.0])[:,None]
        practice = ranking(x, axis=1)
        msg = printfail(theory, practice)    
        self.assert_((theory == practice).all(), msg)
        
    def test_ranking_6(self):
        """afunc.ranking #6"""
        x = np.array([[ 1.0,   nan,   1.0,   nan,   nan],
                      [ 1.0,   1.0,   nan,   nan,   nan],
                      [ 1.0,   2.0,   0.0,   2.0,   nan],
                      [ 1.0,   3.0,   1.0,   1.0,   0.0]])   
        theory = np.array([[ 0.0,   nan,   0.5,  nan,   nan],
                           [ 0.0,  -1.0,   nan,  nan,   nan],
                           [ 0.0,   0.0,  -1.0,  1.0,   nan],
                           [ 0.0,   1.0,   0.5, -1.0,   0.0]])                    
        practice = ranking(x)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)        

    def test_ranking_7(self):
        """afunc.ranking #7"""
        x = np.array([[ 1.0,   nan,   1.0,   nan,   nan],
                      [ 1.0,   1.0,   nan,   nan,   nan],
                      [ 1.0,   2.0,   0.0,   2.0,   nan],
                      [ 1.0,   3.0,   1.0,   1.0,   0.0]])   
        theory = np.array([[ 0.0,   nan ,   0.0,  nan  ,   nan],
                           [ 0.0,   0.0 ,   nan,  nan  ,   nan],
                           [-1.0/3, 2.0/3, -1.0,  2.0/3,   nan],
                           [ 0.0,   1.0 ,   0.0,  0.0  ,  -1.0]])                    
        practice = ranking(x, 1)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)

    def test_ranking_8(self):
        """afunc.ranking #8"""
        x = np.array([[ 1.0,   1.0,   1.0,   1.0],
                      [ 1.0,   1.0,   2.0,   2.0],
                      [ 2.0,   2.0,   3.0,   2.0],
                      [ 2.0,   3.0,   3.0,   3.0]])   
        theory = np.array([[-2.0/3, -2.0/3,   -1.0,  -1.0],
                           [-2.0/3, -2.0/3, -1.0/3,   0.0],
                           [ 2.0/3,  1.0/3,  2.0/3,   0.0],
                           [ 2.0/3,    1.0,  2.0/3,   1.0]])                    
        practice = ranking(x, 0)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg) 
        
    def test_ranking_9(self):
        """afunc.ranking #9"""
        x = np.array([[ 1.0,   1.0,   1.0,   1.0],
                      [ 1.0,   1.0,   2.0,   2.0],
                      [ 2.0,   2.0,   3.0,   2.0],
                      [ 2.0,   3.0,   3.0,   3.0]]) 
        x = x.T  
        theory = np.array([[-2.0/3, -2.0/3,   -1.0,  -1.0],
                           [-2.0/3, -2.0/3, -1.0/3,   0.0],
                           [ 2.0/3,  1.0/3,  2.0/3,   0.0],
                           [ 2.0/3,    1.0,  2.0/3,   1.0]])
        theory = theory.T                                       
        practice = ranking(x, 1)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)              

    def test_ranking_10(self):
        """afunc.ranking #10"""
        x = np.array([[ nan],
                      [ nan],
                      [ nan]])  
        theory = np.array([[ nan],
                           [ nan],
                           [ nan]])                                     
        practice = ranking(x, axis=0)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)

    def test_ranking_11(self):
        """afunc.ranking #11"""
        x = np.array([[ nan, nan],
                      [ nan, nan],
                      [ nan, nan]])  
        theory = np.array([[ nan, nan],
                           [ nan, nan],
                           [ nan, nan]])                                     
        practice = ranking(x, axis=0)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)

    def test_ranking_12(self):
        """afunc.ranking #12"""
        x = np.array([[ nan, nan, nan]])  
        theory = np.array([[ nan, nan, nan]])                                     
        practice = ranking(x, axis=1)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode        
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
class Test_geometric_mean(unittest.TestCase):
    """Test afunc.geometric_mean"""

    def setUp(self):
        self.x = np.array([[1.0, nan, 6.0, 2.0, 8.0],
                           [2.0, 4.0, 8.0, 2.0, 1.0]])
        self.xnan = np.array([[nan, nan, nan, nan, nan],
                              [nan, nan, nan, nan, nan]])
        self.x2 = np.array([[ 2.0,  2.0],
                            [ 1.0,  3.0],
                            [ 3.0,  1.0]])
        self.tol = 1e-8
        self.nancode = -9999                    

    def test_geometric_mean_1(self):
        """afunc.geometric_mean #1"""
        theory = np.array([[ 2.        ],
                           [ 1.73205081],
                           [ 1.73205081]])
        practice =  geometric_mean(self.x2, 1)
        msg = printfail(theory, practice)
        self.assert_((abs(theory - practice) < self.tol).all(), msg)                  

    def test_geometric_mean_2(self):
        """afunc.geometric_mean #2"""
        theory = np.array([[ 2.        ],
                           [ 1.73205081],
                           [ 1.73205081]])
        practice =  geometric_mean(self.x2)
        msg = printfail(theory, practice)
        self.assert_((abs(theory - practice) < self.tol).all(), msg)     

    def test_geometric_mean_3(self):
        """afunc.geometric_mean #3"""
        theory = np.array([[ 1.81712059,  1.81712059]])
        practice =  geometric_mean(self.x2, 0)
        msg = printfail(theory, practice)
        self.assert_((abs(theory - practice) < self.tol).all(), msg)  

    def test_geometric_mean_4(self):
        """afunc.geometric_mean #4"""
        theory = np.array([[   nan],
                           [   nan]])
        practice =  geometric_mean(self.xnan)
        msg = printfail(theory, practice)
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((abs(theory - practice) < self.tol).all(), msg) 
        
    def test_geometric_mean_5(self):
        """afunc.geometric_mean #5"""
        theory = np.array([[ 3.1301691601465746],
                           [ 2.6390158215457888]])
        practice =  geometric_mean(self.x, 1)
        msg = printfail(theory, practice)
        self.assert_((abs(theory - practice) < self.tol).all(), msg)                   

    def test_geometric_mean_6(self):
        """afunc.geometric_mean #6"""
        theory = np.array([[ 1.4142135623730951, 4.0, 6.9282032302755088, 2.0,
                                                           2.8284271247461903]])
        practice =  geometric_mean(self.x, 0)
        msg = printfail(theory, practice)
        self.assert_((abs(theory - practice) < self.tol).all(), msg)
        
    def test_geometric_mean_7(self):
        """afunc.geometric_mean #7"""
        x = np.array([[1e200, 1e200]])
        theory = np.array([[1e200]])
        practice =  geometric_mean(x)
        msg = printfail(theory, practice)
        self.assert_((abs(theory - practice) < 1e187).all(), msg)         
        
class Test_movingsum(unittest.TestCase):
    """Test afunc.movingsum"""        

    def setUp(self):
        self.x = np.array([[1.0, nan, 6.0, 0.0, 8.0],
                           [2.0, 4.0, 8.0, 0.0,-1.0]])
        self.xnan = np.array([[  nan,  nan,  nan,  nan,  nan],
                              [  nan,  nan,  nan,  nan,  nan]])
        self.window = 2
        self.x2 = np.array([[ 2.0,  2.0],
                            [ 1.0,  3.0],
                            [ 3.0,  1.0]])
        self.nancode = -9999                    
        #convert to array
        self.x = np.asarray(self.x)
        self.xnan2 = np.asarray(self.xnan[:,:-1])
        self.x2 = np.asarray(self.x2)

    def test_movingsum_1(self):
        """afunc.movingsum #1"""    
        theory = self.xnan 
        practice = movingsum(self.xnan, self.window, norm=True)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg)              

    def test_movingsum_2(self):
        """afunc.movingsum #2"""    
        theory = self.xnan
        practice = movingsum(self.xnan, self.window, norm=False)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg)    

    def test_movingsum_3(self):
        """afunc.movingsum #3"""    
        theory = np.array([[  nan, 2.0, 12.0, 6.0, 8.0],
                           [  nan, 6.0, 12.0, 8.0,-1.0]])   
        #theory = np.asarray(theory[:,1:])
        practice = movingsum(self.x, self.window, norm=True)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg)

    def test_movingsum_4(self):
        """afunc.movingsum #4"""    
        theory = np.array([[  nan, 1.0,  6.0, 6.0, 8.0],
                           [  nan, 6.0, 12.0, 8.0,-1.0]])
        #theory = np.asarray(theory[:,1:])
        practice = movingsum(self.x, self.window, norm=False)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg)

    def test_movingsum_5(self):
        """afunc.movingsum #5"""    
        theory = np.array([[nan,  nan,  nan,  nan,  nan],
                           [3.0,  8.0,  14.0, 0.0,  7.0]])
        #theory = np.asarray(theory[1,:])
        practice = movingsum(self.x, self.window, axis=0, norm=True)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg)

    def test_movingsum_6(self):
        """afunc.movingsum #6"""    
        theory = np.array([[nan,  nan,  nan,  nan,  nan],
                           [3.0,  4.0,  14.0, 0.0,  7.0]])
        #theory = np.asarray(theory[1,:])
        practice = movingsum(self.x, self.window, axis=0, norm=False)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)
        
    def test_movingsum_7(self):
        """afunc.movingsum #7"""   
        theory = np.array([[nan, 4.0],
                           [nan, 4.0],
                           [nan, 4.0]])
        #theory = np.asarray(theory[:,1:])
        practice = movingsum(self.x2, self.window)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg) 
        
    def _est_movingsum_8(self):
        """afunc.movingsum #8"""
        #skip for now
        theory = np.array([[nan, 1.4142135623730951, 8.4852813742385713, 6.0, 8.0],
                           [nan, 6.0, 12.0, 8.0,-1.0]])
        #theory = np.asarray(theory[:,1:]) 
        practice = movingsum(self.x, self.window, axis=1, norm=True, q=0.5)
        #q is not a valid argument to the new movingsum
        practice = movingsum(self.x, self.window, axis=1, norm=True)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_(np.all(theory == practice), msg)

class Test_movingsum_forward(unittest.TestCase):
    """Test afunc.movingsum_forward""" 
 
    def setUp(self):
        self.x = np.array([[1.0, nan, 6.0, 0.0, 8.0],
                           [2.0, 4.0, 8.0, 0.0,-1.0]])
        self.xnan = np.array([[  nan,  nan,  nan,  nan,  nan],
                              [  nan,  nan,  nan,  nan,  nan]])
        self.window = 2
        self.nancode = -9999           

    def test_movingsum_forward_1(self):
        """afunc.movingsum_forward #1"""
        theory = np.array([[2.0, 12.0, 6.0, 8.0, nan],
                           [6.0, 12.0, 8.0,-1.0, nan]]) 
        skip = 0
        #theory = theory[:,:-1]             
        practice = movingsum_forward(self.x, self.window, skip, norm=True)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)
        
    def test_movingsum_forward_2(self):
        """afunc.movingsum_forward #2"""    
        theory = np.array([[1.0,  6.0, 6.0, 8.0, nan],
                           [6.0, 12.0, 8.0,-1.0, nan]]) 
        #theory = theory[:,:-1]
        skip = 0                     
        practice = movingsum_forward(self.x, self.window, skip, norm=False)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)        

    def test_movingsum_forward_3(self):
        """afunc.movingsum_forward #3"""    
        theory = np.array([[12.0, 6.0, 8.0, nan, nan],
                           [12.0, 8.0,-1.0, nan, nan]]) 
        skip = 1             
        #theory = theory[:,:-1]        
        practice = movingsum_forward(self.x, self.window, skip, norm=True)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)

    def test_movingsum_forward_4(self):
        """afunc.movingsum_forward #4"""    
        theory = np.array([[ 6.0, 6.0, 8.0, nan, nan],
                           [12.0, 8.0,-1.0, nan, nan]]) 
        skip = 1                     
        practice = movingsum_forward(self.x, self.window, skip, norm=False)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)

    def test_movingsum_forward_5(self):
        """afunc.movingsum_forward #5"""    
        theory = np.array([[2.0, 4.0, 8.0, 0.0,-1.0],
                           [nan, nan, nan, nan, nan]])
        skip = 1
        window = 1                    
        practice = movingsum_forward(self.x, window, skip, axis=0)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)          

class Test_movingrank(unittest.TestCase):
    """Test movingrank"""

    def setUp(self):
        self.x = np.array([[1.0, nan, 6.0, 0.0, 8.0],
                           [2.0, 4.0, 8.0, 0.0,-1.0]])
        self.xnan = np.array([[nan, nan, nan, nan, nan],
                              [nan, nan, nan, nan, nan]])
        self.window = 2
        self.x2 = np.array([[nan, 2.0],
                            [1.0, 3.0],
                            [3.0, 1.0]])
        self.nancode = -9999                    
    
    def test_movingrank_1(self):
        """afunc.movingrank #1"""    
        theory = self.xnan 
        practice = movingrank(self.xnan, self.window)
        msg = printfail(theory, practice)    
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg) 
    
    def test_movingrank_2(self):
        """afunc.movingrank #2"""    
        theory = np.array([[  nan,  nan,  nan,-1.0,1.0],
                           [  nan,1.0,1.0,-1.0,-1.0]]) 
        practice = movingrank(self.x, self.window)
        msg = printfail(theory, practice)        
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)           

    def test_movingrank_3(self):
        """afunc.movingrank #3"""    
        theory = np.array([[nan,  nan,  nan,  nan,  nan],
                           [1.0,  nan,  1.0,  0.0,  -1.0]])
        practice = movingrank(self.x, self.window, axis=0)
        msg = printfail(theory, practice)        
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode  
        self.assert_((theory == practice).all(), msg) 
        
    def test_movingrank_4(self):
        """afunc.movingrank #4"""    
        theory = np.array([[nan,  nan],
                           [nan,  1.0],
                           [nan, -1.0]])
        practice = movingrank(self.x2, self.window)
        msg = printfail(theory, practice)        
        theory[np.isnan(theory)] = self.nancode
        practice[np.isnan(practice)] = self.nancode
        self.assert_((theory == practice).all(), msg)           
           


# Unit tests ----------------------------------------------------------------        
    
def testsuite():

    unit = unittest.TestLoader().loadTestsFromTestCase
    s = []
    
    # Sector functions
    s.append(unit(Test_sector_rank))
    s.append(unit(Test_sector_mean)) 
    s.append(unit(Test_sector_median)) 
    
    # Normalize functions
    s.append(unit(Test_ranking_1N))
    s.append(unit(Test_ranking_norm))
    s.append(unit(Test_ranking))    
    s.append(unit(Test_geometric_mean))
    s.append(unit(Test_movingsum))
    s.append(unit(Test_movingsum_forward))
    s.append(unit(Test_movingrank))      
         
    return unittest.TestSuite(s)

def run():   
    suite = testsuite()
    unittest.TextTestRunner(verbosity=2).run(suite)
    