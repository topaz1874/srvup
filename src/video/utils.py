
def get_vid(directon, instance):
    category = instance.category
    vid_sets = category.video_set.all()
    if directon == 'next':
        vid_qs = vid_sets.filter(ordering__gt=instance.id)
        
    elif directon == 'previous' :
        vid_qs = vid_sets.filter(ordering__lt=instance.id).reverse()
    vid = None
    try :
        vid = vid_qs[0]
    except IndexError:
        vid = None
    return vid