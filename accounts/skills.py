# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse

skills = {
    'write' : (u'写手', u'写',
                [(u'长篇', 0), (u'中篇', 1), (u'短篇', 2), (u'文案', 3)]
                ),
    'paint' : (u'画师', u'画',
                 [(u'漫画', 4), (u'厚涂', 5), (u'平涂', 6), (u'赛璐璐', 7), (u'像素', 8), (u'素描', 9), (u'其它技法', 10)]
                 ),
    'design' : (u'设计美工', u'设',
                 [(u'排版', 11), (u'平面设计', 12), (u'网页设计', 13), (u'产品设计', 14)]
                 ),
    'prog' : (u'程序员', u'程',
              [(u'网站编程', 15), (u'游戏编程', 16), (u'系统编程', 17)]
              ),
    'music' : (u'音乐制作', u'音',
              [(u'作曲', 18), (u'编曲', 19), (u'作词', 20), (u'母带/录音制作', 21), (u'Vocal', 22)]
              ),
    '_other' : (u'其他', u'水',
               [(u'围观的能力', 23)]
               ),
}
total_skill = 23

def int2skill(skill):
    if not skill:
        skill = 0
    
    profile_skill = []
    for i, (_, abbreviation, list) in skills.items():
        tem = False
        for _, sid in list:
            if skill & (1<<sid):
                tem = True
                break
        
        if tem:
            profile_skill.append(("shui", 1, abbreviation))
    return profile_skill
    
def set_skill(request, profile):
    skill = profile.skill
    if not skill:
        skill = 0
    
    skill_list = []
    for i, (category, abbreviation, list) in skills.items():
        tem = []
        for item, sid in list:
            if skill & (1<<sid):
                checked = "checked"
            else: checked = ""
            
            tem.append((item, "skill_" + str(sid), checked))
        skill_list.append((category, tem))
    
    if request.method == 'POST':
        skill = 0
        for i, _ in request.POST.items():
            if i.startswith("skill_"):
                sid = int(i[6:])
                if sid > total_skill or sid < 0: continue
                skill = (skill | (1<<sid))
        profile.skill = skill
        profile.save()
        
        for category, list in skill_list:
            for i in xrange(len(list)):
                item, sid, checked = list[i]
                if skill & (1<<int(sid[6:])):
                    list[i] = (item, sid, "checked")
                else:
                    list[i] = (item, sid, "")
            
    return TemplateResponse(request, 'accounts/setting_skill.html', {'skill_list': skill_list, 'active': "skill"})