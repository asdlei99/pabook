#coding=utf-8

class BookCategories:
    categories = ["其他", "玄幻", "武侠", "仙侠", "都市", "军事", "历史", "游戏", "体育", "科幻", "灵异", "言情", "穿越"]
    @classmethod
    def categoryInt(cls, category):
        if "科幻" in category:
            return cls.categories.index("科幻");
        if "幻" in category:
            return cls.categories.index("玄幻");
        elif "武" in category:
            return cls.categories.index("武侠");
        elif "仙" in category:
            return cls.categories.index("仙侠");
        elif "都" in category:
            return cls.categories.index("都市");
        elif "军" in category:
            return cls.categories.index("军事");
        elif "史" in category:
            return cls.categories.index("历史");
        elif "游" in category:
            return cls.categories.index("游戏");
        elif "体" in category:
            return cls.categories.index("体育");
        elif "灵" in category:
            return cls.categories.index("灵异");
        elif "情" in category:
            return cls.categories.index("言情");
        elif "穿" in category:
            return cls.categories.index("穿越");
        else:
            return cls.categories.index("其他");
