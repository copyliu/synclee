# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse

SKILL_CHOICES = (
    (u'write', u'写手'),
    (u'paint', u'画师'),
    (u'design', u'设计美工'),
    (u'prog', u'程序员'),
    (u'music', u'音乐制作'),
    (u'_other', u'其他'),
)

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
total_skill = 24

def skill2str(skill):
    if not skill:
        skill = 0
    return (("%%%ds" % total_skill) % bin(skill)[2:])

def int2skill(skill):
    skill = skill2str(skill)
    
    profile_skill = []
    for i, (_, abbreviation, list) in skills.items():
        tem = False
        for _, sid in list:
            if skill[sid] == '1':
                tem = True
                break
        
        if tem:
            profile_skill.append((i, 1, abbreviation))
    return profile_skill
    
