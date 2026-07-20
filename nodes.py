import os
import json
import random

def load_prompts_from_json(path):
    if not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
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
    PART_COUNT = 12

    @classmethod
    def INPUT_TYPES(cls):
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        required = {
            "prompt_dir": ("STRING", {
                "default": "./part",
                "multiline": False,
            }),
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            "mode": (["concat", "single"], {"default": "single"}),
            "separator": ("STRING", {"default": ", "}),
            "触发词开关": ("BOOLEAN", {"default": False}),
            "触发词内容": ("STRING", {"default": "", "multiline": True}),
            "超强中文模式": ("BOOLEAN", {"default": True}),
            "NSFW": ("BOOLEAN", {"default": False}),
            "使用提示": ("STRING", {
                "default": "提示：开关互斥，多开无效（包括中文模式）此处勿动。",
                "multiline": True,
                "readonly": True,
            }),
        }
        for i in range(1, cls.PART_COUNT + 1):
            required[f"提示词{i}"] = (
                "BOOLEAN",
                {"default": False},
            )
        return {"required": required}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "pick"
    CATEGORY = "Krea2"

    def pick(self, prompt_dir, seed, mode, separator, **kwargs):
        random.seed(seed if seed else None)
        if prompt_dir.startswith("./") or prompt_dir.startswith(".\\"):
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_dir = os.path.abspath(os.path.join(plugin_dir, prompt_dir))
        active_pools = []
        if kwargs.get("超强中文模式", False):
            zc_path = os.path.join(prompt_dir, "part-zc.json")
            pool = load_prompts_from_json(zc_path)
            if pool:
                active_pools.append(pool)
        if kwargs.get("NSFW", False):
            nsfw_path = os.path.join(prompt_dir, "part13.json")
            pool = load_prompts_from_json(nsfw_path)
            if pool:
                active_pools.append(pool)
        for i in range(1, self.PART_COUNT + 1):
            if kwargs.get(f"提示词{i}", False):
                path = os.path.join(prompt_dir, f"part{i:02d}.json")
                pool = load_prompts_from_json(path)
                if pool:
                    active_pools.append(pool)
        if not active_pools:
            return ("（未开启任何提示词源）",)
        if mode == "single":
            result = random.choice(random.choice(active_pools))
        else:
            result = separator.join(random.choice(p) for p in active_pools)
        if kwargs.get("触发词开关", False):
            trigger = str(kwargs.get("触发词内容", "")).strip()
            if trigger:
                result = trigger + separator + result if result else trigger
        return (result,)
