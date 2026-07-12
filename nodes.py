import os
import json
import random

def load_prompts_from_json(path):
    if not os.path.isfile(path):
        print(f"[Krea2] ❌ 文件不存在: {path}")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Krea2] ❌ 读取失败: {path} -> {e}")
        return []

    if isinstance(data, list):
        return [str(x).strip() for x in data if str(x).strip()]

    if isinstance(data, dict):
        for key in ("prompts", "prompt", "list", "items", "data"):
            if key in data and isinstance(data[key], list):
                return [str(x).strip() for x in data[key] if str(x).strip()]
        result = []
        for v in data.values():
            if isinstance(v, list):
                result.extend(str(x).strip() for x in v if str(x).strip())
        return result

    return []

class Krea2PromptPicker:
    PART_COUNT = 12  # ✅ 支持 part01 ~ part12

    @classmethod
    def INPUT_TYPES(cls):
        plugin_dir = os.path.dirname(os.path.abspath(__file__))

        required = {
            "prompt_dir": ("STRING", {
                "default": "./part",
                "multiline": False,
                "placeholder": "./part"
            }),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            "mode": (["concat", "single"], {"default": "single"}),  # ✅ 默认单例
            "separator": ("STRING", {"default": ", "}),
        }

        # ✅ part1~part12 开关
        for i in range(1, cls.PART_COUNT + 1):
            label = "超强" if i == 12 else f"part{i}"
            required[f"part{i}"] = (
                "BOOLEAN",
                {"default": i == 1, "label": label}  # ✅ part1 默认开，part12 叫「超强」
            )

        return {"required": required}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "pick"
    CATEGORY = "Krea2"

    def pick(self, prompt_dir, seed, mode, separator, **kwargs):
        random.seed(seed if seed else None)

        # ✅ ./part 自动转绝对路径
        if prompt_dir.startswith("./") or prompt_dir.startswith(".\\"):
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_dir = os.path.abspath(os.path.join(plugin_dir, prompt_dir))

        print(f"\n[Krea2 落日krea2提示词] 🚀 实际路径: {prompt_dir}")

        active_pools = []

        for i in range(1, self.PART_COUNT + 1):
            if kwargs.get(f"part{i}", False):
                filename = f"part{i:02d}.json"
                full_path = os.path.join(prompt_dir, filename)
                print(f"  ✅ {filename} -> 读取中")

                pool = load_prompts_from_json(full_path)
                if pool:
                    active_pools.append(pool)
                    print(f"     成功读取 {len(pool)} 条")
                else:
                    print(f"     ⚠️ 文件为空或格式错误")

        if not active_pools:
            return ("（没有开启任何 part，或开启的 part 中没有可用提示词）",)

        if mode == "single":
            result = random.choice(random.choice(active_pools))
        else:
            result = separator.join(random.choice(p) for p in active_pools)

        print(f"  ✅ 抽卡完成\n")
        return (result,)