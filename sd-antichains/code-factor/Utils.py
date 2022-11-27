import SdNodeWritable
import SubDagWritable
import DesignPoint
import numpy as np
import json


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SdNodeWritable.SdNodeWritable) or isinstance(obj, SubDagWritable.SubDagWritable) or isinstance (obj, DesignPoint.DesignPoint):
            return obj.__dict__
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else :
            return super(MyEncoder, self).default(obj) 