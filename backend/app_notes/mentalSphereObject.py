import persistent

class MentalSphereObject(persistent.Persistent):
    """
    ZODB persistent object for MentalSphere
    Stores references to PostGIS spatial data IDs
    """
    def __init__(self, id, name, detail, texture, color, rec_status, 
                 created_by_id, position_id, rotation_id, created_at):
        self.id = id
        self.name = name
        self.detail = detail
        self.texture = texture
        self.color = color
        self.rec_status = rec_status
        self.created_by_id = created_by_id
        self.position_id = position_id  # Reference to PostGIS spatial data
        self.rotation_id = rotation_id  # Reference to PostGIS spatial data
        self.created_at = created_at
        self.updated_at = created_at
        
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_detail(self):
        return self.detail
    
    def set_detail(self, detail):
        self.detail = detail
    
    def get_texture(self):
        return self.texture
    
    def set_texture(self, texture):
        self.texture = texture
    
    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color
    
    def get_rec_status(self):
        return self.rec_status
    
    def set_rec_status(self, rec_status):
        self.rec_status = rec_status
    
    def get_created_by_id(self):
        return self.created_by_id
    
    def get_position_id(self):
        return self.position_id
    
    def set_position_id(self, position_id):
        self.position_id = position_id
    
    def get_rotation_id(self):
        return self.rotation_id
    
    def set_rotation_id(self, rotation_id):
        self.rotation_id = rotation_id
    
    def get_created_at(self):
        return self.created_at
    
    def get_updated_at(self):
        return self.updated_at
    
    def set_updated_at(self, updated_at):
        self.updated_at = updated_at


class MindObject(persistent.Persistent):
    """
    ZODB persistent object for Mind
    Represents a collection of MentalSpheres
    """
    def __init__(self, id, name, detail, position, rec_status, 
                 created_by_id, mental_sphere_ids, created_at):
        self.id = id
        self.name = name
        self.detail = detail
        self.position = position  # [x, y, z]
        self.rec_status = rec_status
        self.created_by_id = created_by_id
        self.mental_sphere_ids = mental_sphere_ids if mental_sphere_ids else []
        self.created_at = created_at
        self.updated_at = created_at
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_detail(self):
        return self.detail
    
    def set_detail(self, detail):
        self.detail = detail
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position
    
    def get_rec_status(self):
        return self.rec_status
    
    def set_rec_status(self, rec_status):
        self.rec_status = rec_status
    
    def get_created_by_id(self):
        return self.created_by_id
    
    def get_mental_sphere_ids(self):
        return self.mental_sphere_ids
    
    def add_mental_sphere(self, sphere_id):
        """Add a mental sphere to this mind"""
        if sphere_id not in self.mental_sphere_ids:
            self.mental_sphere_ids.append(sphere_id)
    
    def remove_mental_sphere(self, sphere_id):
        """Remove a mental sphere from this mind"""
        if sphere_id in self.mental_sphere_ids:
            self.mental_sphere_ids.remove(sphere_id)
    
    def set_mental_spheres(self, sphere_ids):
        """Set the list of mental spheres"""
        self.mental_sphere_ids = sphere_ids
    
    def get_created_at(self):
        return self.created_at
    
    def get_updated_at(self):
        return self.updated_at
    
    def set_updated_at(self, updated_at):
        self.updated_at = updated_at
