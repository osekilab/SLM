import json
import pandas as pd
import collections

RandM_irregular_verb_types = {
    'I': ['beat', 'fit', 'set', 'spread', 'hit', 'cut', 'put', 'thrust', 'bid'],
    'II': ['build', 'send', 'spend', 'bend', 'lend'],
    'III': ['feel', 'deal', 'do', 'flee', 'tell', 'sell', 'hear', 'keep', 'leave', 'sleep', 'lose', 'mean', 'say', 'sweep', 'creep', 'weep'],
    'IV': ['have', 'make', 'think', 'buy', 'bring', 'seek', 'teach', 'catch'],
    'V': ['get', 'meet', 'shoot', 'write', 'lead', 'understand', 'sit', 'mislead', 'bleed', 'feed', 'stand', 'light', 'find', 'fight', 'read', 'meet', 'hide', 'hold', 'ride', 'breed', 'wind', 'grind'],
    'VIa': ['drink', 'ring', 'sing', 'swim'],
    'VIb': ['drag', 'hang', 'swin', 'dig', 'cling', 'stick'],
    'VII': ['give', 'take', 'come', 'shake', 'arise', 'rise', 'run', 'become', 'bear', 'wear', 'speak', 'brake', 'drive', 'strike', 'fall', 'freeze', 'choose', 'tear'],
    'VIII': ['go', 'throw', 'blow', 'grow', 'draw', 'fly', 'know', 'see'],
}

other_verb2types = {
    'shut': 'I',
    'upset': 'I',
    'hurt': 'I',
    'bite': 'V',
    'eat': 'V',
    'forget': 'V',
    'shrink': 'VIa',
    'sink': 'VIa',
    'win': 'VIb',
    'spin around': 'VIb',
    'wake up': 'VII',
    'forgive': 'VII',
    'break': 'VII',
    'steal': 'VII',
    'awaken': '-',
}

# shut→shut                 /ʃʌt/→/ʃʌt/... 変化なし→I
# bite→bit                  /bάɪt/→/bít/ ...論文のVのexampleとして記載ありV→V
# wake up→woke up           /wéɪk/→/wóuk/ ...t,dで終わらないかつ，V,VIではない→VII
# win→won                   /wín/→/wˈʌn/ ...VIb?
# spin around→spun around   /spín/→/spˈʌn/ ... VIb?
# forgive→forgave           /fɚgív/→/fɚgéɪv/ ...giveはVII→VII
# shrink→shrank             /ʃríŋk/→/ʃrˈæŋk/ ...VIa?
# upset→upset               /`ʌpsét/→/`ʌpsét/...変化なし→I
# eat→ate                   /íːt/→/éɪt/ ...V?
# sink→sank                 /síŋk/→/sˈæŋk/ ...VIa
# forget→forgot             /fɚgét/→/fɚgάt/ ...getはV→V?
# hurt→hurt                 /hˈɚːt/→/hˈɚːt/ ...変化なし→I
# awaken→awakened           /əwéɪk(ə)n/→/ʌˈwekʌnd/ ...irregularタグがついているが規則動詞に見える?
# break→broke               /bréɪk/→/bróʊk/ ...論文のVIIのexampleとして記載あり→VII
# steal→stole               /stíːl/→/stóʊl/ ...VII?


def save_verb2type(sentences_jsonl_path, out_path):
    # load jsonl
    df = pd.read_json(sentences_jsonl_path, orient="records", lines=True)
    # ターゲットの動詞の原型=copy形を抽出
    target_verbs = df['one_prefix_word_copy'].tolist()
    target_verbs_pl = df['one_prefix_word_good'].tolist()
    
    # R&Mのtableからverb_typeを割り当て
    verb2type = {}
    for target_verb in target_verbs:
        for type_name, verbs in RandM_irregular_verb_types.items():
            if target_verb.split(' ')[0] in verbs:
                verb2type[target_verb] = type_name
                break
    
    # R&Mのtableに載っていない動詞へのverb_typeの割り当て
    print('Verbs that not in R&M table:')
    print('verb', 'plform', 'verb_type', sep='\t')
    for target_verb, pl_form in zip(target_verbs, target_verbs_pl):
        if target_verb not in verb2type:
            print(target_verb, pl_form, other_verb2types[target_verb], sep='\t')
            verb2type[target_verb] = other_verb2types[target_verb]
    
    # 各タイプのカウント
    counter = collections.Counter(verb2type.values())
    print(f'num of verb type in all verbs:')
    print(counter)
    
    with open(out_path, 'w') as f:
        json.dump(verb2type, f)


def add_verb_type_to_baby_error():
    sentences_jsonl_path = 'outputs/baby_error/overregularized_past_verbs.jsonl'
    out_path = 'outputs/verb2type.json'
    save_verb2type(sentences_jsonl_path, out_path)
    
    with open(out_path) as f:
        verb2type = json.load(f)
    
    df = pd.read_json(sentences_jsonl_path, orient="records", lines=True)
    df['verb_type'] = df['one_prefix_word_copy'].apply(lambda verb: verb2type[verb])
    
    # 各タイプのカウント
    counter = collections.Counter(df['verb_type'].tolist())
    print(f'num of verb type in {sentences_jsonl_path}:')
    print(counter)
    
    df.to_json(f'{sentences_jsonl_path.rsplit(".")[0]}_with_verbtypes.jsonl', orient='records', lines=True, index=False)


def main():
    add_verb_type_to_baby_error()
    
    
    ####### print type 2 verbs (論文用) #######
    with open('outputs/verb2type.json') as f:
        verb2type  = json.load(f)
    
    type2verbs = {}
    for verb, type_name in verb2type.items():
        verb = verb.split(' ')[0]
        if type_name not in type2verbs:
            type2verbs[type_name] = [verb]
        elif verb not in type2verbs[type_name]:
            type2verbs[type_name].append(verb)
    
    print(type2verbs)
    ##########################################


if __name__ == '__main__':
    main()
    
    
'''
{
'VIII': [throw go grow know draw],
'V': [meet light stand hide ride write shoot read sit get fight hold understand breed lead find bite eat forget], 
'VII': [speak freeze drive tear shake come wear choose fall strike take wake forgive break steal], 
'IV': [bring have buy make catch teach], 
'VIa': [sing drink shrink sink], 
'III': [flee leave lose hear sell weep keep sweep], 
'II': [build bend spend], 
'I': [shut upset hurt], 
'VIb': [win spin], 
'-': [awaken]}'''