from Bio import Phylo
import io
import random

def pro_dic_genome_taxa(domain,release,taxa_level):
    if domain == "archaea":
        d = 'ar53'
    else:
        d = 'bac120'
    taxa_list = ['p', 'c', 'o', 'f', 'g', 's']
    if taxa_level.lower() in taxa_list:
        t = taxa_list.index(taxa_level.lower()) + 1
    
    dic_genome_taxa = {}
    dic_taxa_genome = {}
    with open(f"{d}_taxonomy_r{release}.tsv")as obj:
        for line in obj.readlines():
            line = line.strip('\n').split('\t')
            genome = line[0]
            taxa = line[1].split(";")[t]
            taxa = taxa.split('__')[-1]
            dic_genome_taxa[genome] = taxa
            if taxa in dic_taxa_genome:
                dic_taxa_genome[taxa].append(genome)
            else:
                dic_taxa_genome[taxa] = [genome]
    return [dic_taxa_genome,dic_genome_taxa]


def is_interested_clade(clade,dic_genome_taxa,interested_classes):
    if clade.name in dic_genome_taxa:
        #if dic_genome_taxa[clade.name] in interested_classes:
            #print(clade.name+'\t'+dic_genome_taxa[clade.name])
        return dic_genome_taxa[clade.name] in interested_classes
    return False

def delete_tree_leaves(domain,release,taxa_level,genome_num,interested_classes):
    if domain == "archaea":
        d = 'ar53'
    else:
        d = 'bac120'
    dic_taxa_genome = pro_dic_genome_taxa(domain,release,taxa_level)[0]
    dic_genome_taxa = pro_dic_genome_taxa(domain,release,taxa_level)[1]
    tree_file = f'{d}_r{release}.tree'
    tree = Phylo.read(tree_file, 'newick')
    
    m,n = 0,0
    # 收集需要修剪的节点
    to_prune = []
    dic_taxa_num = {}
    for clade in tree.find_clades():
        if clade.is_terminal():  # 只检查叶节点
            m += 1
            taxa = dic_genome_taxa[clade.name]
            if is_interested_clade(clade, dic_genome_taxa, interested_classes):
                if taxa in dic_taxa_num:
                    dic_taxa_num[taxa] += 1
                    if len(dic_taxa_genome[taxa]) >= genome_num:
                        if dic_taxa_num[taxa] >= genome_num:
                            to_prune.append(clade)
                            n += 1
                else:
                    dic_taxa_num[taxa] = 0
            if not is_interested_clade(clade, dic_genome_taxa, interested_classes):
                n += 1
                to_prune.append(clade)

    # 进行修剪
    for clade in to_prune:
        tree.prune(clade)

    print(m, n)  # 打印总的叶节点数和被修剪的节点数

    # 保存修剪后的树
    Phylo.write(tree, f'trimmed_{d}_r{release}_leaf_{genome_num}_newick.tree', 'newick')
    Phylo.write(tree, f'trimmed_{d}_r{release}_leaf_{genome_num}_nexus.tree', 'nexus')
    Phylo.write(tree, f'trimmed_{d}_r{release}_leaf_{genome_num}_phyloxml.tree', 'phyloxml')

def pro_tree_label(domain,release,taxa_level,genome_num):
    if domain == "archaea":
        d = 'ar53'
    else:
        d = 'bac120'
    dic_genome_taxa = pro_dic_genome_taxa(domain,release,taxa_level)[1]

    with open("ITOL_labels_template.txt", 'r', encoding='utf-8') as f_fixed:
        fixed_content = f_fixed.read()
    
    tree = Phylo.read(f'trimmed_{d}_r{release}_leaf_{genome_num}_newick.tree', 'newick')
    with open(f'ITOL_{domain}_labels_r{release}_leaf_{genome_num}.txt', 'w', encoding='utf-8') as fout:
        fout.write(fixed_content + '\n')  # 在固定内容后换行
        for clade in tree.find_clades():
            if clade.is_terminal():  # 只检查叶节点
                fout.write(clade.name+','+dic_genome_taxa[clade.name]+'\n')


def obtain_leaf_num(tree_file):
    tree = Phylo.read(tree_file, 'newick')
    terminals = tree.get_terminals()
    number_of_terminals = len(terminals)
    return number_of_terminals


def pro_tree_main(d,release,taxa_level,min_genome_total_num,max_genome_taxa_num):
    interested_classes = []
    pwd = "/dssg/home/acct-trench/trench-6/wangyecheng/Global_Hydrothermal/host_virus/"
    with open(f"{pwd}result_stat_taxa_genome_num_virus_infected.txt")as obj:
        next(obj)
        for line in obj.readlines():
            line = line.strip('\n').split('\t')
            domain = line[0]
            layer = line[1]
            taxa = line[2]
            genome_num = int(line[3])
            if domain.lower() == d and layer == taxa_level and genome_num >= min_genome_total_num and taxa != "Unclassified":
                interested_classes.append(taxa)
    print("===="+str(len(interested_classes)))
    delete_tree_leaves(d,release,taxa_level,max_genome_taxa_num,interested_classes)
    
def pro_tree_infor_main(d,release,taxa_level,max_genome_taxa_num):
    pro_tree_label(d,release,taxa_level,max_genome_taxa_num)


pro_tree_main("archaea","220","c",10,1)
pro_tree_main("bacteria","220","c",10,1)

pro_tree_infor_main("archaea","220","c",1)
pro_tree_infor_main("bacteria","220","c",1)


print(obtain_leaf_num('ar53_r220.tree'))
print(obtain_leaf_num('bac120_r220.tree'))
