import numpy as np

from .. import functions as fn
from ..Qt import QtWidgets
from .DataTreeWidget import DataTreeWidget

__all__ = ['DiffTreeWidget']


class DiffTreeWidget(QtWidgets.QWidget):
    """
    Widget for displaying differences between hierarchical python data structures
    (eg, nested dicts, lists, and arrays)
    """
    def __init__(self, parent=None, a=None, b=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.trees = [DataTreeWidget(self), DataTreeWidget(self)]
        for t in self.trees:
            self.layout.addWidget(t)
        if a is not None:
            self.setData(a, b)
    
    def setData(self, a, b):
        """
        Set the data to be compared in this widget.
        """
        self.data = (a, b)
        self.trees[0].setData(a)
        self.trees[1].setData(b)
        
        return self.compare(a, b)
        
    def compare(self, a, b, path=()):
        """
        Compare data structure *a* to structure *b*. 
        
        Return True if the objects match completely. 
        Otherwise, return a structure that describes the differences:
        
            { 'type': bool
              'len': bool,
              'str': bool,
              'shape': bool,
              'dtype': bool,
              'mask': array,
              }
        
                
        """
        bad = (255, 200, 200)
        # generate typestr, desc, childs for each object
        typeA, descA, childsA, _ = self.trees[0].parse(a)
        typeB, descB, childsB, _ = self.trees[1].parse(b)
        
        if typeA != typeB:
            self.setColor(path, 1, bad)
        if descA != descB:
            self.setColor(path, 2, bad)
            
        if isinstance(a, dict) and isinstance(b, dict):
            keysA = set(a.keys())
            keysB = set(b.keys())
            for key in keysA - keysB:
                self.setColor(path+(key,), 0, bad, tree=0)
            for key in keysB - keysA:
                self.setColor(path+(key,), 0, bad, tree=1)
            for key in keysA & keysB:
                self.compare(a[key], b[key], path+(key,))
            
        elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            for i in range(max(len(a), len(b))):
                if len(a) <= i:
                    self.setColor(path+(i,), 0, bad, tree=1)
                elif len(b) <= i:
                    self.setColor(path+(i,), 0, bad, tree=0)
                else:
                    self.compare(a[i], b[i], path+(i,))
                    
        elif isinstance(a, np.ndarray) and isinstance(b, np.ndarray) and a.shape == b.shape:
            tableNodes = [tree.nodes[path].child(0) for tree in self.trees]
            if a.dtype.fields is None and b.dtype.fields is None:
                eq = self.compareArrays(a, b)
                if not np.all(eq):
                    for n in tableNodes:
                        n.setBackground(0, fn.mkBrush(bad))
                #for i in np.argwhere(~eq):
                    
            else:
                if a.dtype == b.dtype:
                    for i,k in enumerate(a.dtype.fields.keys()):
                        eq = self.compareArrays(a[k], b[k])
                        if not np.all(eq):
                            for n in tableNodes:
                                n.setBackground(0, fn.mkBrush(bad))
                        #for j in np.argwhere(~eq):
                    
        # dict: compare keys, then values where keys match
        # list: 
        # array: compare elementwise for same shape

    def compareArrays(self, a, b):
        intnan = -9223372036854775808  # happens when np.nan is cast to int
        anans = np.isnan(a) | (a == intnan)
        bnans = np.isnan(b) | (b == intnan)
        eq = anans == bnans
        mask = ~anans
        eq[mask] = np.allclose(a[mask], b[mask])
        return eq
    
    def setColor(self, path, column, color, tree=None):
        brush = fn.mkBrush(color)
        
        # Color only one tree if specified.
        if tree is None:
            trees = self.trees
        else:
            trees = [self.trees[tree]]
        
        for tree in trees:
            item = tree.nodes[path]
            item.setBackground(column, brush)
    
    def _compare(self, a, b):
        """
        Compare data structure *a* to structure *b*. 
        """
        info = a
        expect = b
        # Check test structures are the same
        if type(info) is not type(expect):
            raise AssertionError("objects have different types")
        if hasattr(info, '__len__'):
            if len(info) != len(expect):
                raise AssertionError("objects have different lengths")
            
        if isinstance(info, dict):
            for k in info:
                if k not in expect:
                    raise AssertionError("key missing from expected object")
            for k in expect:
                if k not in info:
                    raise AssertionError("key missing from actual object")
                self.compare_results(info[k], expect[k])
        elif isinstance(info, list):
            for i in range(len(info)):
                self.compare_results(info[i], expect[i])
        elif isinstance(info, np.ndarray):
            if info.shape != expect.shape:
                raise AssertionError("arrays have different shapes")
            if info.dtype != expect.dtype:
                raise AssertionError("arrays have different dtypes")
            if info.dtype.fields is None:
                intnan = -9223372036854775808  # happens when np.nan is cast to int
                inans = np.isnan(info) | (info == intnan)
                enans = np.isnan(expect) | (expect == intnan)
                if not np.all(inans == enans):
                    raise AssertionError("arrays have different nan masks")
                mask = ~inans
                if not np.allclose(info[mask], expect[mask]):
                    raise AssertionError("arrays are not close")
            else:
                for k in info.dtype.fields.keys():
                    self.compare_results(info[k], expect[k])
        else:
            try:
                equal = info == expect
            except Exception as exc:
                raise NotImplementedError("Cannot compare objects of type %s" % type(info)) from exc
            if not equal:
                raise NotImplementedError("Cannot compare objects of type %s" % type(info))
    
