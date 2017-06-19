"""
Module for upsampling data.
"""

import numpy

def upsamplingSecondOrderLagrange(data, refine_ratio, component_idx=0):
    """
    Upsampling the data using second order Lagrange interpolation.
    """
    
    r = refine_ratio
    
    stencil_size = 2
    half_stencil_size = stencil_size/2
    
    data_shape = data.shape
    data_shape = numpy.delete(data_shape, [0])
    
    dim = data_shape.shape[0]
    
    # Compute the coefficients for second order Lagrange interpolation.
    
    c_0 = None
    c_1 = None
    c_2 = None
    
    c_0 = numpy.ones([r[0], stencil_size], dtype=data.dtype)
    if dim == 2:
        c_1 = numpy.ones([r[1], stencil_size], dtype=data.dtype)
    if dim == 3:
        c_2 = numpy.ones([r[2], stencil_size], dtype=data.dtype)
    
    if r[0] % 2 == 0: # If the upsampled nodes don't overlap with the original nodes.
        
        delta = 1.0/r[0]
        for s in range(r[0]):
            idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
            for i in range(stencil_size):
                for j in range(stencil_size):
                    if (i != j):
                        c_0[s, i] = c_0[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 2:
            delta = 1.0/r[1]
            for s in range(r[1]):
                idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_1[s, i] = c_1[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 3:
            delta = 1.0/r[2]
            for s in range(r[2]):
                idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_2[s, i] = c_2[s, i] * (idx_r - j)/(i - j)
    
    else: # If some of the upsampled nodes overlap with the original nodes.
        
        delta = 1.0/r[0]
        for s in range(r[0]):
            idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
            for i in range(stencil_size):
                for j in range(stencil_size):
                    if (i != j):
                        c_0[s, i] = c_0[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 2:
            delta = 1.0/r[1]
            for s in range(r[1]):
                idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_1[s, i] = c_1[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 3:
            delta = 1.0/r[2]
            for s in range(r[2]):
                idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_2[s, i] = c_2[s, i] * (idx_r - j)/(i - j)
    
    # Initialize containers to store the upsampled data. The elements in the container
    # are initialized as NAN values.
    
    upsampled_data_shape_0 = None
    upsampled_data_shape_1 = None
    upsampled_data_shape = None
    
    upsampled_data_0 = None
    upsampled_data_1 = None
    upsampled_data = None
    
    if dim == 1:
        upsampled_data_shape = numpy.multiply(data_shape, r[0])
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        upsampled_data[:] = numpy.NAN
    
    elif dim == 2:
        upsampled_data_shape_0 = numpy.copy(data_shape)
        upsampled_data_shape_0[0] = upsampled_data_shape_0[0]*r[0]
        
        upsampled_data_shape = numpy.copy(upsampled_data_shape_0)
        upsampled_data_shape[1] = upsampled_data_shape[1]*r[1]
        
        upsampled_data_0 = numpy.empty(upsampled_data_shape_0, dtype = data.dtype)
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        
        upsampled_data_0[:] = numpy.NAN
        upsampled_data[:] = numpy.NAN
        
    elif dim == 3:
        upsampled_data_shape_0 = numpy.copy(data_shape)
        upsampled_data_shape_0[0] = upsampled_data_shape_0[0]*r[0]
        
        upsampled_data_shape_1 = numpy.copy(upsampled_data_shape_0)
        upsampled_data_shape_1[1] = upsampled_data_shape_1[1]*r[1]
        
        upsampled_data_shape = numpy.copy(upsampled_data_shape_1)
        upsampled_data_shape[2] = upsampled_data_shape[2]*r[2]
        
        upsampled_data_0 = numpy.empty(upsampled_data_shape_0, dtype = data.dtype)
        upsampled_data_1 = numpy.empty(upsampled_data_shape_1, dtype = data.dtype)
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        
        upsampled_data_0[:] = numpy.NAN
        upsampled_data_1[:] = numpy.NAN
        upsampled_data[:] = numpy.NAN
    
    # Get the component's data.
    
    data_component = None
    if dim== 1:
        data_component = data[component_idx, :]
    elif dim == 2:
        data_component = data[component_idx, :, :]
    elif dim == 3:
        data_component = data[component_idx, :, :, :]
    
    # Upsample the data with sixth order Lagrange interpolation.
    
    if dim == 1:
        start_idx_fine = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        for s in range(r[0]):
            upsampled_data[(start_idx_fine + s):end_idx_fine:r[0]] = c_0[s, 0]*data_component[0:(-stencil_size + 1)] \
                + c_0[s, 1]*data_component[1:]
    
    elif dim == 2:
        start_idx_fine_0 = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        start_idx_fine_1 = (half_stencil_size - 1)*r[1] + (r[1] + 1)/2
        end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
        
        for s in range(r[0]):
            upsampled_data_0[(start_idx_fine_0 + s):end_idx_fine_0:r[0], :] = \
                c_0[s, 0]*data_component[0:(-stencil_size + 1), :] + c_0[s, 1]*data_component[1:, :]
        
        for s in range(r[1]):
            upsampled_data[start_idx_fine_0:end_idx_fine_0, (start_idx_fine_1 + s):end_idx_fine_1:r[1]] = \
                c_1[s, 0]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 0:(-stencil_size + 1)] \
                + c_1[s, 1]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 1:]
    
    elif dim == 3:
        start_idx_fine_0 = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        start_idx_fine_1 = (half_stencil_size - 1)*r[1] + (r[1] + 1)/2
        end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
        
        start_idx_fine_2 = (half_stencil_size - 1)*r[2] + (r[2] + 1)/2
        end_idx_fine_2 = upsampled_data_shape[2] - (half_stencil_size - 1)*r[2] - r[2]/2
        
        for s in range(r[0]):
            upsampled_data_0[(start_idx_fine_0 + s):end_idx_fine_0:r[0], : :] = \
                c_0[s, 0]*data_component[0:(-stencil_size + 1), :, :] \
                + c_0[s, 1]*data_component[1:, :, :]
        
        for s in range(r[1]):
            upsampled_data_1[start_idx_fine_0:end_idx_fine_0, (start_idx_fine_1 + s):end_idx_fine_1:r[1], :] = \
                c_1[s, 0]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 0:(-stencil_size + 1), :] \
                + c_1[s, 1]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 1:, :]
        
        for s in range(r[2]):
            upsampled_data[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, (start_idx_fine_2 + s):end_idx_fine_2:r[2]] = \
                c_2[s, 0]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 0:(-stencil_size + 1)] \
                + c_2[s, 1]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 1:]
    
    # If some of the upsampled nodes overlap with the original nodes, copy the data from the original nodes to the first
    # sets of overlapped nodes since they are not upsampled yet.
    
    if r[0] % 2 == 1: # If some of the upsampled nodes overlap with the original nodes.
        overlap_idx_coarse = half_stencil_size - 1
        overlap_idx_fine = (half_stencil_size - 1)*r[0] + r[0]/2
        
        if dim == 1:
            upsampled_data[overlap_idx_fine] = data_component[overlap_idx_coarse]
        
        elif dim == 2:
            start_idx_fine_0 = (half_stencil_size - 1)*r[0] + r[0]/2
            end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
            
            start_idx_fine_1 = (half_stencil_size - 1)*r[1] + r[1]/2
            end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
            
            upsampled_line_data_0 = numpy.repeat(data_component[overlap_idx_coarse, :], \
                r[1])
            
            upsampled_line_data_1 = numpy.repeat(data_component[:, overlap_idx_coarse], \
                r[0])
            
            upsampled_data[overlap_idx_fine, start_idx_fine_1:end_idx_fine_1] = \
                upsampled_line_data_0[start_idx_fine_1:end_idx_fine_1]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, overlap_idx_fine] = \
                upsampled_line_data_1[start_idx_fine_0:end_idx_fine_0]
        
        elif dim == 3:
            start_idx_fine_0 = (half_stencil_size - 1)*r[0] + r[0]/2
            end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
            
            start_idx_fine_1 = (half_stencil_size - 1)*r[1] + r[1]/2
            end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
            
            start_idx_fine_2 = (half_stencil_size - 1)*r[2] + r[2]/2
            end_idx_fine_2 = upsampled_data_shape[2] - (half_stencil_size - 1)*r[2] - r[2]/2
            
            upsampled_face_data_0 = numpy.repeat(data_component[overlap_idx_coarse, :, :], \
                r[1], axis = 0)
            upsampled_face_data_0 = numpy.repeat(upsampled_face_data_0, r[2], axis = 1)
            
            upsampled_face_data_1 = numpy.repeat(data_component[:, overlap_idx_coarse, :], \
                r[0], axis = 0)
            upsampled_face_data_1 = numpy.repeat(upsampled_face_data_1, r[2], axis = 1)
            
            upsampled_face_data_2 = numpy.repeat(data_component[:, :, overlap_idx_coarse], \
                r[0], axis = 0)
            upsampled_face_data_2 = numpy.repeat(upsampled_face_data_2, r[1], axis = 1)
            
            upsampled_data[overlap_idx_fine, start_idx_fine_1:end_idx_fine_1, start_idx_fine_2:end_idx_fine_2] = \
                upsampled_face_data_0[start_idx_fine_1:end_idx_fine_1, start_idx_fine_2:end_idx_fine_2]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, overlap_idx_fine, start_idx_fine_2:end_idx_fine_2] = \
                upsampled_face_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_2:end_idx_fine_2]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, overlap_idx_fine] = \
                upsampled_face_data_2[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1]
    
    return upsampled_data


def upsamplingFourthOrderLagrange(data, refine_ratio, component_idx=0):
    """
    Upsampling the data using fourth order Lagrange interpolation.
    """
    
    r = refine_ratio
    
    stencil_size = 4
    half_stencil_size = stencil_size/2
    
    data_shape = data.shape
    data_shape = numpy.delete(data_shape, [0])
    
    dim = data_shape.shape[0]
    
    # Compute the coefficients for fourth order Lagrange interpolation.
    
    c_0 = None
    c_1 = None
    c_2 = None
    
    c_0 = numpy.ones([r[0], stencil_size], dtype=data.dtype)
    if dim == 2:
        c_1 = numpy.ones([r[1], stencil_size], dtype=data.dtype)
    if dim == 3:
        c_2 = numpy.ones([r[2], stencil_size], dtype=data.dtype)
    
    if r[0] % 2 == 0: # If the upsampled nodes don't overlap with the original nodes.
        
        delta = 1.0/r[0]
        for s in range(r[0]):
            idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
            for i in range(stencil_size):
                for j in range(stencil_size):
                    if (i != j):
                        c_0[s, i] = c_0[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 2:
            delta = 1.0/r[1]
            for s in range(r[1]):
                idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_1[s, i] = c_1[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 3:
            delta = 1.0/r[2]
            for s in range(r[2]):
                idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_2[s, i] = c_2[s, i] * (idx_r - j)/(i - j)
    
    else: # If some of the upsampled nodes overlap with the original nodes.
        
        delta = 1.0/r[0]
        for s in range(r[0]):
            idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
            for i in range(stencil_size):
                for j in range(stencil_size):
                    if (i != j):
                        c_0[s, i] = c_0[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 2:
            delta = 1.0/r[1]
            for s in range(r[1]):
                idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_1[s, i] = c_1[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 3:
            delta = 1.0/r[2]
            for s in range(r[2]):
                idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_2[s, i] = c_2[s, i] * (idx_r - j)/(i - j)
        
    # Initialize containers to store the upsampled data. The elements in the container
    # are initialized as NAN values.
    
    upsampled_data_shape_0 = None
    upsampled_data_shape_1 = None
    upsampled_data_shape = None
    
    upsampled_data_0 = None
    upsampled_data_1 = None
    upsampled_data = None
    
    if dim == 1:
        upsampled_data_shape = numpy.multiply(data_shape, r[0])
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        upsampled_data[:] = numpy.NAN
    
    elif dim == 2:
        upsampled_data_shape_0 = numpy.copy(data_shape)
        upsampled_data_shape_0[0] = upsampled_data_shape_0[0]*r[0]
        
        upsampled_data_shape = numpy.copy(upsampled_data_shape_0)
        upsampled_data_shape[1] = upsampled_data_shape[1]*r[1]
        
        upsampled_data_0 = numpy.empty(upsampled_data_shape_0, dtype = data.dtype)
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        
        upsampled_data_0[:] = numpy.NAN
        upsampled_data[:] = numpy.NAN
        
    elif dim == 3:
        upsampled_data_shape_0 = numpy.copy(data_shape)
        upsampled_data_shape_0[0] = upsampled_data_shape_0[0]*r[0]
        
        upsampled_data_shape_1 = numpy.copy(upsampled_data_shape_0)
        upsampled_data_shape_1[1] = upsampled_data_shape_1[1]*r[1]
        
        upsampled_data_shape = numpy.copy(upsampled_data_shape_1)
        upsampled_data_shape[2] = upsampled_data_shape[2]*r[2]
        
        upsampled_data_0 = numpy.empty(upsampled_data_shape_0, dtype = data.dtype)
        upsampled_data_1 = numpy.empty(upsampled_data_shape_1, dtype = data.dtype)
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        
        upsampled_data_0[:] = numpy.NAN
        upsampled_data_1[:] = numpy.NAN
        upsampled_data[:] = numpy.NAN
    
    # Get the component's data.
    
    data_component = None
    if dim== 1:
        data_component = data[component_idx, :]
    elif dim == 2:
        data_component = data[component_idx, :, :]
    elif dim == 3:
        data_component = data[component_idx, :, :, :]
    
    # Upsample the data with sixth order Lagrange interpolation.
    
    if dim == 1:
        start_idx_fine = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        for s in range(r[0]):
            upsampled_data[(start_idx_fine + s):end_idx_fine:r[0]] = c_0[s, 0]*data_component[0:(-stencil_size + 1)] \
                + c_0[s, 1]*data_component[1:(-stencil_size + 2)] + c_0[s, 2]*data_component[2:(-stencil_size + 3)] \
                + c_0[s, 3]*data_component[3:]
    
    elif dim == 2:
        start_idx_fine_0 = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        start_idx_fine_1 = (half_stencil_size - 1)*r[1] + (r[1] + 1)/2
        end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
        
        for s in range(r[0]):
            upsampled_data_0[(start_idx_fine_0 + s):end_idx_fine_0:r[0], :] = \
                c_0[s, 0]*data_component[0:(-stencil_size + 1), :] + c_0[s, 1]*data_component[1:(-stencil_size + 2), :] \
                + c_0[s, 2]*data_component[2:(-stencil_size + 3), :] + c_0[s, 3]*data_component[3:, :]
        
        for s in range(r[1]):
            upsampled_data[start_idx_fine_0:end_idx_fine_0, (start_idx_fine_1 + s):end_idx_fine_1:r[1]] = \
                c_1[s, 0]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 0:(-stencil_size + 1)] \
                + c_1[s, 1]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 1:(-stencil_size + 2)] \
                + c_1[s, 2]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 2:(-stencil_size + 3)] \
                + c_1[s, 3]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 3:]
    
    elif dim == 3:
        start_idx_fine_0 = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        start_idx_fine_1 = (half_stencil_size - 1)*r[1] + (r[1] + 1)/2
        end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
        
        start_idx_fine_2 = (half_stencil_size - 1)*r[2] + (r[2] + 1)/2
        end_idx_fine_2 = upsampled_data_shape[2] - (half_stencil_size - 1)*r[2] - r[2]/2
        
        for s in range(r[0]):
            upsampled_data_0[(start_idx_fine_0 + s):end_idx_fine_0:r[0], : :] = \
                c_0[s, 0]*data_component[0:(-stencil_size + 1), :, :] \
                + c_0[s, 1]*data_component[1:(-stencil_size + 2), :, :] \
                + c_0[s, 2]*data_component[2:(-stencil_size + 3), :, :] \
                + c_0[s, 3]*data_component[3:, :, :]
        
        for s in range(r[1]):
            upsampled_data_1[start_idx_fine_0:end_idx_fine_0, (start_idx_fine_1 + s):end_idx_fine_1:r[1], :] = \
                c_1[s, 0]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 0:(-stencil_size + 1), :] \
                + c_1[s, 1]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 1:(-stencil_size + 2), :] \
                + c_1[s, 2]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 2:(-stencil_size + 3), :] \
                + c_1[s, 3]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 3:, :]
        
        for s in range(r[2]):
            upsampled_data[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, (start_idx_fine_2 + s):end_idx_fine_2:r[2]] = \
                c_2[s, 0]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 0:(-stencil_size + 1)] \
                + c_2[s, 1]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 1:(-stencil_size + 2)] \
                + c_2[s, 2]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 2:(-stencil_size + 3)] \
                + c_2[s, 3]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 3:]
    
    # If some of the upsampled nodes overlap with the original nodes, copy the data from the original nodes to the first
    # sets of overlapped nodes since they are not upsampled yet.
    
    if r[0] % 2 == 1: # If some of the upsampled nodes overlap with the original nodes.
        overlap_idx_coarse = half_stencil_size - 1
        overlap_idx_fine = (half_stencil_size - 1)*r[0] + r[0]/2
        
        if dim == 1:
            upsampled_data[overlap_idx_fine] = data_component[overlap_idx_coarse]
        
        elif dim == 2:
            start_idx_fine_0 = (half_stencil_size - 1)*r[0] + r[0]/2
            end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
            
            start_idx_fine_1 = (half_stencil_size - 1)*r[1] + r[1]/2
            end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
            
            upsampled_line_data_0 = numpy.repeat(data_component[overlap_idx_coarse, :], \
                r[1])
            
            upsampled_line_data_1 = numpy.repeat(data_component[:, overlap_idx_coarse], \
                r[0])
            
            upsampled_data[overlap_idx_fine, start_idx_fine_1:end_idx_fine_1] = \
                upsampled_line_data_0[start_idx_fine_1:end_idx_fine_1]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, overlap_idx_fine] = \
                upsampled_line_data_1[start_idx_fine_0:end_idx_fine_0]
        
        elif dim == 3:
            start_idx_fine_0 = (half_stencil_size - 1)*r[0] + r[0]/2
            end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
            
            start_idx_fine_1 = (half_stencil_size - 1)*r[1] + r[1]/2
            end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
            
            start_idx_fine_2 = (half_stencil_size - 1)*r[2] + r[2]/2
            end_idx_fine_2 = upsampled_data_shape[2] - (half_stencil_size - 1)*r[2] - r[2]/2
            
            upsampled_face_data_0 = numpy.repeat(data_component[overlap_idx_coarse, :, :], \
                r[1], axis = 0)
            upsampled_face_data_0 = numpy.repeat(upsampled_face_data_0, r[2], axis = 1)
            
            upsampled_face_data_1 = numpy.repeat(data_component[:, overlap_idx_coarse, :], \
                r[0], axis = 0)
            upsampled_face_data_1 = numpy.repeat(upsampled_face_data_1, r[2], axis = 1)
            
            upsampled_face_data_2 = numpy.repeat(data_component[:, :, overlap_idx_coarse], \
                r[0], axis = 0)
            upsampled_face_data_2 = numpy.repeat(upsampled_face_data_2, r[1], axis = 1)
            
            upsampled_data[overlap_idx_fine, start_idx_fine_1:end_idx_fine_1, start_idx_fine_2:end_idx_fine_2] = \
                upsampled_face_data_0[start_idx_fine_1:end_idx_fine_1, start_idx_fine_2:end_idx_fine_2]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, overlap_idx_fine, start_idx_fine_2:end_idx_fine_2] = \
                upsampled_face_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_2:end_idx_fine_2]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, overlap_idx_fine] = \
                upsampled_face_data_2[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1]
    
    return upsampled_data


def upsamplingSixthOrderLagrange(data, refine_ratio, component_idx=0):
    """
    Upsampling the data using sixth order Lagrange interpolation.
    """
    
    r = refine_ratio
    
    stencil_size = 6
    half_stencil_size = stencil_size/2
    
    data_shape = data.shape
    data_shape = numpy.delete(data_shape, [0])
    
    dim = data_shape.shape[0]
    
    # Compute the coefficients for sixth order Lagrange interpolation.
    
    c_0 = None
    c_1 = None
    c_2 = None
    
    c_0 = numpy.ones([r[0], stencil_size], dtype=data.dtype)
    if dim == 2:
        c_1 = numpy.ones([r[1], stencil_size], dtype=data.dtype)
    if dim == 3:
        c_2 = numpy.ones([r[2], stencil_size], dtype=data.dtype)
    
    if r[0] % 2 == 0: # If the upsampled nodes don't overlap with the original nodes.
        
        delta = 1.0/r[0]
        for s in range(r[0]):
            idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
            for i in range(stencil_size):
                for j in range(stencil_size):
                    if (i != j):
                        c_0[s, i] = c_0[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 2:
            delta = 1.0/r[1]
            for s in range(r[1]):
                idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_1[s, i] = c_1[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 3:
            delta = 1.0/r[2]
            for s in range(r[2]):
                idx_r = (half_stencil_size - 1) + (s + 0.5)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_2[s, i] = c_2[s, i] * (idx_r - j)/(i - j)
    
    else: # If some of the upsampled nodes overlap with the original nodes.
        
        delta = 1.0/r[0]
        for s in range(r[0]):
            idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
            for i in range(stencil_size):
                for j in range(stencil_size):
                    if (i != j):
                        c_0[s, i] = c_0[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 2:
            delta = 1.0/r[1]
            for s in range(r[1]):
                idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_1[s, i] = c_1[s, i] * (idx_r - j)/(i - j)
        
        if dim >= 3:
            delta = 1.0/r[2]
            for s in range(r[2]):
                idx_r = (half_stencil_size - 1) + (s + 1.0)*delta
                for i in range(stencil_size):
                    for j in range(stencil_size):
                        if (i != j):
                            c_2[s, i] = c_2[s, i] * (idx_r - j)/(i - j)
    
    # Initialize containers to store the upsampled data. The elements in the container
    # are initialized as NAN values.
    
    upsampled_data_shape_0 = None
    upsampled_data_shape_1 = None
    upsampled_data_shape = None
    
    upsampled_data_0 = None
    upsampled_data_1 = None
    upsampled_data = None
    
    if dim == 1:
        upsampled_data_shape = numpy.multiply(data_shape, r[0])
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        upsampled_data[:] = numpy.NAN
    
    elif dim == 2:
        upsampled_data_shape_0 = numpy.copy(data_shape)
        upsampled_data_shape_0[0] = upsampled_data_shape_0[0]*r[0]
        
        upsampled_data_shape = numpy.copy(upsampled_data_shape_0)
        upsampled_data_shape[1] = upsampled_data_shape[1]*r[1]
        
        upsampled_data_0 = numpy.empty(upsampled_data_shape_0, dtype = data.dtype)
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        
        upsampled_data_0[:] = numpy.NAN
        upsampled_data[:] = numpy.NAN
        
    elif dim == 3:
        upsampled_data_shape_0 = numpy.copy(data_shape)
        upsampled_data_shape_0[0] = upsampled_data_shape_0[0]*r[0]
        
        upsampled_data_shape_1 = numpy.copy(upsampled_data_shape_0)
        upsampled_data_shape_1[1] = upsampled_data_shape_1[1]*r[1]
        
        upsampled_data_shape = numpy.copy(upsampled_data_shape_1)
        upsampled_data_shape[2] = upsampled_data_shape[2]*r[2]
        
        upsampled_data_0 = numpy.empty(upsampled_data_shape_0, dtype = data.dtype)
        upsampled_data_1 = numpy.empty(upsampled_data_shape_1, dtype = data.dtype)
        upsampled_data = numpy.empty(upsampled_data_shape, dtype = data.dtype)
        
        upsampled_data_0[:] = numpy.NAN
        upsampled_data_1[:] = numpy.NAN
        upsampled_data[:] = numpy.NAN
    
    # Get the component's data.
    
    data_component = None
    if dim== 1:
        data_component = data[component_idx, :]
    elif dim == 2:
        data_component = data[component_idx, :, :]
    elif dim == 3:
        data_component = data[component_idx, :, :, :]
    
    # Upsample the data with sixth order Lagrange interpolation.
    
    if dim == 1:
        start_idx_fine = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        for s in range(r[0]):
            upsampled_data[(start_idx_fine + s):end_idx_fine:r[0]] = c_0[s, 0]*data_component[0:(-stencil_size + 1)] \
                + c_0[s, 1]*data_component[1:(-stencil_size + 2)] + c_0[s, 2]*data_component[2:(-stencil_size + 3)] \
                + c_0[s, 3]*data_component[3:(-stencil_size + 4)] + c_0[s, 4]*data_component[4:(-stencil_size + 5)] \
                + c_0[s, 5]*data_component[5:]
    
    elif dim == 2:
        start_idx_fine_0 = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        start_idx_fine_1 = (half_stencil_size - 1)*r[1] + (r[1] + 1)/2
        end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
        
        for s in range(r[0]):
            upsampled_data_0[(start_idx_fine_0 + s):end_idx_fine_0:r[0], :] = \
                c_0[s, 0]*data_component[0:(-stencil_size + 1), :] + c_0[s, 1]*data_component[1:(-stencil_size + 2), :] \
                + c_0[s, 2]*data_component[2:(-stencil_size + 3), :] + c_0[s, 3]*data_component[3:(-stencil_size + 4), :] \
                + c_0[s, 4]*data_component[4:(-stencil_size + 5), :] + c_0[s, 5]*data_component[5:, :]
        
        for s in range(r[1]):
            upsampled_data[start_idx_fine_0:end_idx_fine_0, (start_idx_fine_1 + s):end_idx_fine_1:r[1]] = \
                c_1[s, 0]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 0:(-stencil_size + 1)] \
                + c_1[s, 1]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 1:(-stencil_size + 2)] \
                + c_1[s, 2]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 2:(-stencil_size + 3)] \
                + c_1[s, 3]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 3:(-stencil_size + 4)] \
                + c_1[s, 4]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 4:(-stencil_size + 5)] \
                + c_1[s, 5]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 5:]
    
    elif dim == 3:
        start_idx_fine_0 = (half_stencil_size - 1)*r[0] + (r[0] + 1)/2
        end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
        
        start_idx_fine_1 = (half_stencil_size - 1)*r[1] + (r[1] + 1)/2
        end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
        
        start_idx_fine_2 = (half_stencil_size - 1)*r[2] + (r[2] + 1)/2
        end_idx_fine_2 = upsampled_data_shape[2] - (half_stencil_size - 1)*r[2] - r[2]/2
        
        for s in range(r[0]):
            upsampled_data_0[(start_idx_fine_0 + s):end_idx_fine_0:r[0], : :] = \
                c_0[s, 0]*data_component[0:(-stencil_size + 1), :, :] \
                + c_0[s, 1]*data_component[1:(-stencil_size + 2), :, :] \
                + c_0[s, 2]*data_component[2:(-stencil_size + 3), :, :] \
                + c_0[s, 3]*data_component[3:(-stencil_size + 4), :, :] \
                + c_0[s, 4]*data_component[4:(-stencil_size + 5), :, :] \
                + c_0[s, 5]*data_component[5:, :, :]
        
        for s in range(r[1]):
            upsampled_data_1[start_idx_fine_0:end_idx_fine_0, (start_idx_fine_1 + s):end_idx_fine_1:r[1], :] = \
                c_1[s, 0]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 0:(-stencil_size + 1), :] \
                + c_1[s, 1]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 1:(-stencil_size + 2), :] \
                + c_1[s, 2]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 2:(-stencil_size + 3), :] \
                + c_1[s, 3]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 3:(-stencil_size + 4), :] \
                + c_1[s, 4]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 4:(-stencil_size + 5), :] \
                + c_1[s, 5]*upsampled_data_0[start_idx_fine_0:end_idx_fine_0, 5:, :]
        
        for s in range(r[2]):
            upsampled_data[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, (start_idx_fine_2 + s):end_idx_fine_2:r[2]] = \
                c_2[s, 0]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 0:(-stencil_size + 1)] \
                + c_2[s, 1]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 1:(-stencil_size + 2)] \
                + c_2[s, 2]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 2:(-stencil_size + 3)] \
                + c_2[s, 3]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 3:(-stencil_size + 4)] \
                + c_2[s, 4]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 4:(-stencil_size + 5)] \
                + c_2[s, 5]*upsampled_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, 5:]
    
    # If some of the upsampled nodes overlap with the original nodes, copy the data from the original nodes to the first
    # sets of overlapped nodes since they are not upsampled yet.
    
    if r[0] % 2 == 1: # If some of the upsampled nodes overlap with the original nodes.
        overlap_idx_coarse = half_stencil_size - 1
        overlap_idx_fine = (half_stencil_size - 1)*r[0] + r[0]/2
        
        if dim == 1:
            upsampled_data[overlap_idx_fine] = data_component[overlap_idx_coarse]
        
        elif dim == 2:
            start_idx_fine_0 = (half_stencil_size - 1)*r[0] + r[0]/2
            end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
            
            start_idx_fine_1 = (half_stencil_size - 1)*r[1] + r[1]/2
            end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
            
            upsampled_line_data_0 = numpy.repeat(data_component[overlap_idx_coarse, :], \
                r[1])
            
            upsampled_line_data_1 = numpy.repeat(data_component[:, overlap_idx_coarse], \
                r[0])
            
            upsampled_data[overlap_idx_fine, start_idx_fine_1:end_idx_fine_1] = \
                upsampled_line_data_0[start_idx_fine_1:end_idx_fine_1]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, overlap_idx_fine] = \
                upsampled_line_data_1[start_idx_fine_0:end_idx_fine_0]
        
        elif dim == 3:
            start_idx_fine_0 = (half_stencil_size - 1)*r[0] + r[0]/2
            end_idx_fine_0 = upsampled_data_shape[0] - (half_stencil_size - 1)*r[0] - r[0]/2
            
            start_idx_fine_1 = (half_stencil_size - 1)*r[1] + r[1]/2
            end_idx_fine_1 = upsampled_data_shape[1] - (half_stencil_size - 1)*r[1] - r[1]/2
            
            start_idx_fine_2 = (half_stencil_size - 1)*r[2] + r[2]/2
            end_idx_fine_2 = upsampled_data_shape[2] - (half_stencil_size - 1)*r[2] - r[2]/2
            
            upsampled_face_data_0 = numpy.repeat(data_component[overlap_idx_coarse, :, :], \
                r[1], axis = 0)
            upsampled_face_data_0 = numpy.repeat(upsampled_face_data_0, r[2], axis = 1)
            
            upsampled_face_data_1 = numpy.repeat(data_component[:, overlap_idx_coarse, :], \
                r[0], axis = 0)
            upsampled_face_data_1 = numpy.repeat(upsampled_face_data_1, r[2], axis = 1)
            
            upsampled_face_data_2 = numpy.repeat(data_component[:, :, overlap_idx_coarse], \
                r[0], axis = 0)
            upsampled_face_data_2 = numpy.repeat(upsampled_face_data_2, r[1], axis = 1)
            
            upsampled_data[overlap_idx_fine, start_idx_fine_1:end_idx_fine_1, start_idx_fine_2:end_idx_fine_2] = \
                upsampled_face_data_0[start_idx_fine_1:end_idx_fine_1, start_idx_fine_2:end_idx_fine_2]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, overlap_idx_fine, start_idx_fine_2:end_idx_fine_2] = \
                upsampled_face_data_1[start_idx_fine_0:end_idx_fine_0, start_idx_fine_2:end_idx_fine_2]
            
            upsampled_data[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1, overlap_idx_fine] = \
                upsampled_face_data_2[start_idx_fine_0:end_idx_fine_0, start_idx_fine_1:end_idx_fine_1]
    
    return upsampled_data

