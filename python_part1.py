# Question 1
def is_expanding_functional(ls):
    differences = [abs(ls[i + 1] - ls[i]) for i in range(0, len(ls) - 1)]
    check_rise = [1 for y in range(0, len(differences) - 1) if differences[y] >= differences[y + 1]]
    return check_rise == []


def is_expanding_effcient(ls):
    length = len(ls)
    if len(ls) > 2:
        for i in range(length - 2):
            if i == 0:
                difference_1 = abs(ls[i + 1] - ls[i])
            difference_next = abs(ls[i + 2] - ls[i + 1])
            if difference_1 >= difference_next:
                return False
            difference_1 = difference_next
        return True
    elif length != 0:
        return True
    else:
        return False


def is_expanding_index(ls):
    for i in range(len(ls) - 2):
        if i == 0:
            difference_1 = abs(ls[i + 1] - ls[i])
        difference_next = abs(ls[i + 2] - ls[i + 1])
        if difference_1 >= difference_next:
            return i - 1
        difference_1 = difference_next
    return i


def count_expanding_series(ls):
    count = 0
    ls_2 = ls.copy()
    while 1:
        if len(ls_2) > 2:
            count = count + 1
            index = is_expanding_index(ls_2)
            if index + 1 == len(ls_2):
                return count
            else:
                ls_2 = ls_2[index + 3:]
        elif len(ls_2) != 0:
            count = count + 1
            return count
        else:
            return count


#print(count_expanding_series([1,90,900]))









## Question 2
def count_dif_letters(smaller_ls_str,larger_ls_str,index,k):#use in part a to count different letters in same location
    for i in range(len(smaller_ls_str)):
        if smaller_ls_str[i].lower()!=larger_ls_str[i].lower():
            index+=1
            if index>k:
                return False
    return True


def is_k_reverse(st1, st2, k):
    index=abs(len(st1)-len(st2))
    if index>k:
        return False
    list_st1 = list(st1[::-1])
    list_st2 = list(st2)
    if len(st1)<len(st2):#in case of that st1 shorter than st2
        return(count_dif_letters(list_st1,list_st2,index,k))
    else:# in case that st1 longer than st2 or has the same length
        return (count_dif_letters(list_st2,list_st1,index,k))





def is_k_mirror_list(ls, k):
    for i in range(len(ls)//2+1):
        if (is_k_reverse(ls[i], ls[len(ls)-1-i], k))==False:
            return False
    return True




# st1='ABBB'
# st2='bbba'
# k=2
# print(is_k_reverse(st1,st2,k))
# ls = ['A','']
# k=1
# print(is_k_mirror_list(ls, k))






## Question 3

def create_encryption_mapping(offset):
    import string
    text = string.ascii_lowercase
    dict_letters={}
    for let in text:
        if ord(let)+offset<123:
            dict_letters[let]=chr(ord(let)+offset)
        else:
            dict_letters[let]=chr(ord(let)-(26-offset))
    return (dict_letters)




def making_new_list(ls,dic):     #### use in part b and
    if ls==[]:
        return []
    new_ls = []
    new_word = []
    for word in ls:
        for let in word:
            if let.isalpha():
                new_word.append(dic.get(let.lower()))
            else:
                new_word.append(let)
        new_word_str = "".join(new_word)
        new_ls.append(new_word_str)
        new_word = []
    return new_ls

def encrypt_list(ls, encrypt_dict):
     return making_new_list(ls,encrypt_dict)



def decrypt_list(ls, encrypt_dict):

    keys=(list(encrypt_dict.keys()))
    values=(list(encrypt_dict.values()))
    flip_dict = {k: v for k, v in zip(values, keys)}
    #print(reverse_dict)
    return making_new_list(ls,flip_dict)


def zipping(dic):#use in part d,in order to convert dictionary to tuple


    x = (list(dic.keys()))
    y = (list(dic.values()))
    zipped = zip(x, y)
    tup_zip = (tuple(zipped))
    return tup_zip


def find_optimal_encryption(ls, bit_dict):
    from collections import Counter
    final_dict={}
    cnt = Counter()
    for word in ls:
       for let in word:
           if let.isalpha():
               cnt[let.lower()] += 1

    freq_dict=dict(cnt)
    print(freq_dict)
    tup_zip_freq=zipping(freq_dict)#calling for zipping function
    f = lambda x: x[1]
    sorted_tup_freq=(sorted(tup_zip_freq,key=f,reverse=True))
    tup_zip_bit = zipping(bit_dict)#calling for zipping function
    sorted_tup_bit = (sorted(tup_zip_bit, key=f, reverse=False))
    for i in range(len(sorted_tup_freq)):
        final_dict[sorted_tup_freq[i][0]] =sorted_tup_bit[i][0]
    return (final_dict)










# dic=create_encryption_mapping(3)
# ls = ['aa/bbB', 'aabbbb', 'bbacc']
# print(encrypt_list(ls, create_encryption_mapping(3)))
# print(decrypt_list(encrypt_list(ls, dic), dic))
# bit_dict = {'a': 30, 'b': 8, 'c': 2}
# print(find_optimal_encryption(ls,bit_dict))





