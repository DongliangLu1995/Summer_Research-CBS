# Summer_Research-CBS
#This is my code for the research "How Lobbists Influence the Rule-making Process in Financial Regulation" during May 2018 to August 2018




#Brief introduction(Ordered by letter order):
1. add_org_tag(434 lines): this program assigns the category(11 different kinds) to companies (like the companies belongs to government, law, financial, or something else) 
2. bag_of_words(145 lines): this program extracts bags of words from comment's txt
3. citation_original_comments(266 lines): this program compares citation content to original comments and to see if there's any similar parts
4. classification(710 lines): this program uses different classifiers to see if using the features can give a good prediction to which rule the comments are from
5. comments on fed(78 lines): this program scrapes comments on the federal researve rules
6. comments_on_reggov(460 lines): this program scrapes comments on regulation.gov
7. crawler cftc(67 lines): this program scrapes meeting on CFTC website
8. effects_comments_similar_parts(288 lines): this program finds similar parts between rules and comments
9. FDIC(170 lines): this program scrapes meeting and comments on FDIC website
10. final_rule_banking: this program downloads final rule from https://www.stlouisfed.org/federal-banking-regulations
11. final_rule_dic(282 lines): this program changes the final rule into bags of words
12. finding_similarfractions(206 lines): this program tests the effect of smith-waterman algorithm
13. get_citation_content(1239 lines): this program extracts the citations in final rules and assign them to the organizations
14. group_comments_SEC_version(686 lines): this program matches the the comments to the organizations they belong to 
14. group_comments_SEC_version2(1004 lines): this program matches the the comments to the organizations they belong to with a higher accuracy
15. group_meetings_SEC_version1(534 lines): this program deals with meetings and clean the names of organizations to a good format
16. group_meetings_SEC_version2(787 lines): this program deals with meetings and clean the names of organizations to a good format with higher accuracy
17. merge_citation_similarity_individual(172 lines): this program calculates individual's comments' similarity with the final rules
18. merge_com_meet_SEC: this program merges the comments and meetings together
19. merge_similarity_citation: this program merges citation with the other features
20. ML_prepare_data(50 lines): this program prepares the data for ML algorithms
21. org_to_citation_location(36 lines): this program shows an example of how to use citation location and its related organizations
22. read_final_rule_version1(653 lines): this program extracts the citations and organizations from the final rule
23. read_final_rule_version2(916 lines): this program extracts the citations and organizations from the final rule
24. read_final_rule_version3(1418 lines): this program extracts the citations and organizations from the final rule with a higher accuracy
25. readxml(32 lines): this program tries to real xml files
26. regression_SEC(458 lines): this program merges x and y data and plot some pictures
27. regression_volcker(35 lines): this program merges x and y data for volcker rule only
28. regression_volcker2(259 lines): this program merges x and y data for volcker rule only
29. scraping _SEC_comments(1217 lines): this program scrapes comments and meetings and assign them to correct organizations
30. sentence_to_paragraph(305 lines): this program merged text of rules
31. separate_paragraph(699 lines): this program tries to further clean the rules
32. similarity(294 lines): this program calculates different similarity measures
33. similarity(353 lines): this program calculates different similarity measures aggregating the same organizations
34. smith_waterman_algo_v2(155 lines): this program modifies the s-w algo making it robust to mis-spellings
35. SEC_comments_meeting(259 lines): this program downloads the SEC comments and meetings
35. toy_example(167 lines): this program shows some similarity measure
36. separate_paragraph_0-30(about 700 lines each): cleaning the final rule text and label each sentence the roles, and determine whether an organizations lobby successfully or not




organized by different roles:
#Programs scraping data from the agencies website:
5. comments on fed(78 lines)
6. comments_on_reggov(460 lines)
7. crawler cftc(67 lines)
9. FDIC(170 lines)
10. final_rule_banking
29. scraping _SEC_comments(1217 lines)
35. SEC_comments_meeting(259 lines)


#Programs cleaning the data:
1. add_org_tag(434 lines)
2. bag_of_words(145 lines)
3. citation_original_comments(266 lines)
11. final_rule_dic(282 lines)
13. get_citation_content(1239 lines)
14. group_comments_SEC_version2(686 lines)
14. group_comments_SEC_version2(1004 lines)
15. group_meetings_SEC_version1(534 lines)
16. group_meetings_SEC_version2(787 lines)
17. merge_citation_similarity_individual(172 lines)
18. merge_com_meet_SEC
19. merge_similarity_citation
20. ML_prepare_data(50 lines)
21. org_to_citation_location(36 lines)
22. read_final_rule_version1(653 lines)
23. read_final_rule_version2(916 lines)
24. read_final_rule_version3(1418 lines)
25. readxml(32 lines)
27. regression_volcker(35 lines)
30. sentence_to_paragraph(305 lines)
31. separate_paragraph(699 lines)
32. similarity(294 lines)
33. similarity(353 lines)
34. smith_waterman_algo_v2(155 lines)
35. toy_example(167 lines)


#Programs showing some results:
4. classification(710 lines)
8. effects_comments_similar_parts(288 lines)
12. finding_similarfractions(206 lines)
26. regression_SEC(458 lines)
28. regression_volcker2(259 lines)
36. separate_paragraph_0-30(about 700 lines each)




















