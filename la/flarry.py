"Functions that operate on larrys."

import numpy as np

from la.deflarry import larry
from la.flabel import flattenlabel
from la.farray import covMissing


# Labels --------------------------------------------------------------------
    
def union(axis, *args):
    """
    Union of labels along specified axis.
    
    Parameters
    ----------
    axis : int
        The axis along which to take the union of the labels.
    args : larrys
        The larrys (separated by commas) over which the union is taken.
        
    Returns
    -------
    out : list
        A list containing the union of the labels.
        
    See Also
    --------
    la.intersection : Intersection of labels along specified axis.
    
    Examples
    --------            
    >>> import la
    >>> y1 = larry([[1, 2], [3, 4]], [['a', 'b'], ['c', 'd']])
    >>> y2 = larry([[1, 2], [3, 4]], [['e', 'b'], ['f', 'd']])
    >>> la.union(0, y1, y2)
    ['a', 'b', 'e']
    >>> la.union(1, y1, y2)
    ['c', 'd', 'f']
    
    """
    rc = frozenset([])
    for arg in args:
        if isinstance(arg, larry):
            rc = frozenset(arg.label[axis]) | rc
        else:
            raise TypeError, 'One or more input is not a larry'
    rc = list(rc)
    rc.sort()
    return rc

def intersection(axis, *args):
    """
    Intersection of labels along specified axis.
    
    Parameters
    ----------
    axis : int
        The axis along which to take the intersection of the labels.
    args : larrys
        The larrys (separated by commas) over which the intersection is taken.
        
    Returns
    -------
    out : list
        A list containing the intersection of the labels.
        
    See Also
    --------
    la.union : Union of labels along specified axis.
    
    Examples
    --------            
    >>> import la
    >>> y1 = larry([[1, 2], [3, 4]], [['a', 'b'], ['c', 'd']])
    >>> y2 = larry([[1, 2], [3, 4]], [['e', 'b'], ['f', 'd']])
    >>> la.intersection(0, y1, y2)
    ['b']
    >>> la.intersection(1, y1, y2)
    ['d']
    
    """
    rc = frozenset(args[0].label[axis])
    for i in xrange(1, len(args)):
        arg = args[i]
        if isinstance(arg, larry):
            rc = frozenset(arg.label[axis]) & rc
        else:
            raise TypeError, 'One or more input is not a larry'
    rc = list(rc)
    rc.sort()
    return rc

# Concatenating -------------------------------------------------------------
    
def stack(mode, **kwargs):
    """Stack 2d larrys to make a 3d larry.
    
    Parameters
    ----------
    mode : {'union', 'intersection'}
        Should the 3d larry be made from the union or intersection of all the
        rows and all the columns?
    kwargs : name=larry
        Variable length input listing the z axis name and larry. For example,
        stack('union', distance=x, temperature=y, pressure=z)
        
    Returns
    -------
    out : larry
        Returns a 3d larry.
        
    Raises
    ------
    ValueError
        If mode is not union or intersection or if any of the input larrys are
        not 2d.
        
    Examples
    --------
    >>> import la
    >>> y1 = la.larry([[1, 2], [3, 4]])
    >>> y2 = la.larry([[5, 6], [7, 8]])
    >>> la.stack('union', name1=y1, othername=y2)
    label_0
        othername
        name1
    label_1
        0
        1
    label_2
        0
        1
    x
    array([[[ 5.,  6.],
            [ 7.,  8.]],
    .
           [[ 1.,  2.],
            [ 3.,  4.]]])    
                        
    """
    if not np.all([kwargs[key].ndim == 2 for key in kwargs]):
        raise ValueError, 'All input larrys must be 2d'
    if mode == 'union':
        logic = union
    elif mode == 'intersection':
        logic = intersection
    else:    
        raise ValueError, 'mode must be union or intersection'   
    row = logic(0, *kwargs.values())
    col = logic(1, *kwargs.values())
    x = np.zeros((len(kwargs), len(row), len(col)))
    zlabel = []
    for i, key in enumerate(kwargs):
        y = kwargs[key]
        y = y.morph(row, 0)
        y = y.morph(col, 1)
        x[i] = y.x
        zlabel.append(key)
    label = [zlabel, row, col]
    return larry(x, label) 
    
def panel(lar):
    """
    Convert a 3d larry of shape (n, m, k) to a 2d larry of shape (m*k, n).
    
    Parameters
    ----------
    lar : 3d larry
        The input must be a 3d larry.
        
    Returns
    -------
    y : 2d larry
        If the input larry has shape (n, m, k) then a larry of shape (m*k, n)
        is returned.
        
    See Also
    --------
    la.larry.swapaxes : Swap the two specified axes.
    la.larry.flatten : Collapsing into one dimension.  
        
    Examples
    --------
    First make a 3d larry:
    
    >>> import numpy as np
    >>> y = larry(np.arange(24).reshape(2,3,4))
    >>> y
    label_0
        0
        1
    label_1
        0
        1
        2
    label_2
        0
        1
        2
        3
    x
    array([[[ 0,  1,  2,  3],
            [ 4,  5,  6,  7],
            [ 8,  9, 10, 11]],
    .
           [[12, 13, 14, 15],
            [16, 17, 18, 19],
            [20, 21, 22, 23]]])
            
    Then make a panel:        
            
    >>> la.func.panel(y)
    label_0
        (0, 0)
        (0, 1)
        (0, 2)
        ...
        (2, 1)
        (2, 2)
        (2, 3)
    label_1
        0
        1
    x
    array([[ 0, 12],
           [ 4, 16],
           [ 8, 20],
           [ 1, 13],
           [ 5, 17],
           [ 9, 21],
           [ 2, 14],
           [ 6, 18],
           [10, 22],
           [ 3, 15],
           [ 7, 19],
           [11, 23]])            
    
    """
    if lar.ndim != 3:
        raise ValueError, "lar must be 3d."
    y = lar.copy()
    y.label = [flattenlabel([y.label[1], y.label[2]])[0], y.label[0]]
    y.x = y.x.T.reshape(-1, y.shape[0])
    return y

# Calc -------------------------------------------------------------
        
def cov(lar):
    """
    Covariance matrix adjusted for missing (NaN) values.
    
    Note: Only works on 2d larrys.
    
    The mean of each row is assumed to be zero. So rows are not demeaned
    and therefore the covariance is normalized by the number of columns,
    not by the number of columns minus 1.        
    
    Parameters
    ----------
    lar : larry
        The larry you want to find the covariance of.
        
    Returns
    -------
    out : larry
        For 2d input of shape (N, T), for example, returns a NxN covariance
        matrix.
        
    Raises
    ------
    ValueError
        If input is not 2d    

    """
    if lar.ndim != 2:
        raise ValueError, 'This function only works on 2d larrys'      
    y = lar.copy()
    y.label[1] = list(y.label[0])
    y.x = covMissing(y.x)
    return y

# Random -----------------------------------------------------------    
    
def rand(*args, **kwargs):
    """
    Random samples from a uniform distribution in a given shape.
    
    The random samples are from a uniform distribution over ``[0, 1)``.
    
    Parameters
    ----------
    args : `n` ints, optional
        The dimensions of the returned larry, should be all positive. These
        may be omitted if you pass in a label as a keyword argument.
    kwargs : keyword arguments, optional
        Keyword arguments to use in the construction of the larry such as
        label and integrity. If a label is passed then its dimensions must
        match the `n` integers passed in or, optionally, you can pass in the
        label without the `n` shape integers. If rand is passed in then that
        will be used to generate the random numbers. In that way you can set
        the state of the random number generator outside of this function.  
    
    Returns
    -------
    Z : larry or float
        A ``(d1, ..., dn)``-shaped larry of floating-point samples from
        a uniform distribution, or a single such float if no parameters were
        supplied.
    
    See Also
    --------
    la.randn : Random samples from the "standard normal" distribution.
    
    Examples
    --------
    A single random sample:
    
    >>> la.rand()
    0.64323350463488804
    
    A shape (2, 2) random larry:
    
    >>> la.rand(2, 2)
    label_0
        0
        1
    label_1
        0
        1
    x
    array([[ 0.09277439,  0.94194077],
           [ 0.72887997,  0.41124147]])
           
    A shape (2, 2) random larry with given labels:
           
    >>> la.rand(label=[['row1', 'row2'], ['col1', 'col2']])
    label_0
        row1
        row2
    label_1
        col1
        col2
    x
    array([[ 0.3449072 ,  0.40397174],
           [ 0.7791279 ,  0.86084403]])
           
    Results are repeatable if you set the state of the random number generator
    outside of la.rand:
           
    >>> import numpy as np
    >>> rs = np.random.RandomState([1, 2, 3])
    >>> la.randn(randn=rs.randn)
    0.89858244820995015
    >>> la.randn(randn=rs.randn)
    0.25528876596298244
    >>> rs = np.random.RandomState([1, 2, 3])
    >>> la.randn(randn=rs.randn)
    0.89858244820995015
    >>> la.randn(randn=rs.randn)
    0.25528876596298244
        
    """
    if 'rand' in kwargs:
        randfunc = kwargs['rand']
        kwargs = dict(kwargs)
        del kwargs['rand']
    else:
        randfunc = np.random.rand   
    if len(args) > 0:
        return larry(randfunc(*args), **kwargs)
    elif 'label' in kwargs:
        n = [len(z) for z in kwargs['label']]
        return larry(randfunc(*n), **kwargs)     
    elif (len(args) == 0) and (len(kwargs) == 0):
        return randfunc()
    elif (len(args) == 0) and (len(kwargs) == 1) and ('rand' in kwargs):
        return randfunc()    
    else:
        raise ValueError, 'Input parameters not recognized'
    
def randn(*args, **kwargs):
    """
    Random samples from the "standard normal" distribution in a given shape.
    
    The random samples are from a "normal" (Gaussian) distribution of mean 0
    and variance 1.
    
    Parameters
    ----------
    args : `n` ints, optional
        The dimensions of the returned larry, should be all positive. These
        may be omitted if you pass in a label as a keyword argument.
    kwargs : keyword arguments, optional
        Keyword arguments to use in the construction of the larry such as
        label and integrity. If a label is passed then its dimensions must
        match the `n` integers passed in or, optionally, you can pass in the
        label without the `n` shape integers. If randn is passed in then that
        will be used to generate the random numbers. In that way you can set
        the state of the random number generator outside of this function.  
    
    Returns
    -------
    Z : larry or float
        A ``(d1, ..., dn)``-shaped larry of floating-point samples from
        the standard normal distribution, or a single such float if
        no parameters were supplied.
    
    See Also
    --------
    la.rand : Random values from a uniform distribution in a given shape.
    
    Examples
    --------
    A single random sample:    
    
    >>> la.randn()
    0.33086946957034052
    
    A shape (2, 2) random larry:    
    
    >>> la.randn(2, 2)
    label_0
        0
        1
    label_1
        0
        1
    x
    array([[-0.08182341,  0.79768108],
           [-0.23584547,  1.80118376]])
           
    A shape (2, 2) random larry with given labels:           
           
    >>> la.randn(label=[['row1', 'row2'], ['col1', 'col2']])
    label_0
        row1
        row2
    label_1
        col1
        col2
    x
    array([[ 0.10737701, -0.24947824],
           [ 1.51021208,  1.00280387]])

    Results are repeatable if you set the state of the random number generator
    outside of la.rand:

    >>> import numpy as np
    >>> rs = np.random.RandomState([1, 2, 3])
    >>> la.randn(randn=rs.randn)
    0.89858244820995015
    >>> la.randn(randn=rs.randn)
    0.25528876596298244
    >>> rs = np.random.RandomState([1, 2, 3])
    >>> la.randn(randn=rs.randn)
    0.89858244820995015
    >>> la.randn(randn=rs.randn)
    0.25528876596298244
    
    """
    if 'randn' in kwargs:
        randnfunc = kwargs['randn']
        kwargs = dict(kwargs)
        del kwargs['randn']        
    else:
        randnfunc = np.random.randn   
    if len(args) > 0:
        return larry(randnfunc(*args), **kwargs)
    elif 'label' in kwargs:
        n = [len(z) for z in kwargs['label']]
        return larry(randnfunc(*n), **kwargs)     
    elif (len(args) == 0) and (len(kwargs) == 0):
        return randnfunc()
    elif (len(args) == 0) and (len(kwargs) == 1) and ('randn' in kwargs):
        return randnfunc()         
    else:
        raise ValueError, 'Input parameters not recognized'
                            