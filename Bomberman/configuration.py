Images = {
        "name" :  "Bomberman.png",
        "scale_factor" : 2, # everything is scaled using this factor
        "fieldsize" : 16, #pixels
        "transparent_color" : (56, 135, 0),
        "fields" : {
            'W': (3,3, 1), 
            'w': (4,3, 6),
            'b': (0,3, 3),   
            'L': (0,0, 3),
            'D': (3,0, 3),
            'R': (0,1, 3),
            'U': (3,1, 3),
            ' ': (7,1, 1),
            'X': (0,2, 6),
        },
        "cross" : [(2,6), (7,6), (2,11), (7,11)],
        "animations" : {
            "b" : {"time": '200ms',  "type": "custom", "timeline" : "0121",},
            "w" : {"time": '100ms',  "type": "normal"},
            "f" : {"time": '100ms',  "type": "custom", 
                   "timeline" : "01233210"}, # for all parts of the cross
            "LDRU" : {"time": '100ms',  "type": "normal"},  # for player animations
            "X" : {"time": '100ms',  "type": "normal"},
            },        
    }

Text = {
    "name" : "Font.png",
    "scale_factor" : 4,
    "letter_size" : 24,
    "dims" : (16, 6),
    "invalid_char" : '?',
    "chars_table" :  [
             (32, 0), 
             (65, 65),
             (97, 33),
             (123, 91),
             (128, 0)       # last char is 127 - this is just a sentinel
         ]    
    }