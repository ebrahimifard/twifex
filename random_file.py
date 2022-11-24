class NetworkAnalsysis():
    def batch_cooccurrence_network(self, batch):
        '''Building the co-occurrence network'''

        network = nx.Graph()
        fringe_network = nx.Graph()
        russian_network = nx.Graph()
        fringe_russian_network = nx.Graph()

        for ind1, group_1 in enumerate(tqdm(batch)):
            for ind2, group_2 in enumerate(batch):
                if ind2 > ind1:

                    group_id1, group_name1 = group_1.split("@@")
                    group_id2, group_name2 = group_2.split("@@")

                    network.add_nodes_from([group_name1, group_name2])
                    fringe_network.add_nodes_from([group_name1, group_name2])
                    russian_network.add_nodes_from([group_name1, group_name2])
                    fringe_russian_network.add_nodes_from([group_name1, group_name2])

                    for post1 in batch[group_1]:
                        creation_time1 = post1[0]
                        msg_urls1 = post1[1]
                        desc_urls1 = post1[2]

                        for post2 in batch[group_2]:
                            creation_time2 = post2[0]
                            msg_urls2 = post2[1]
                            desc_urls2 = post2[2]


                            for msg_url1 in msg_urls1:
                                for msg_url2 in msg_urls2:
                                    if msg_url1 == msg_url2:
                                        msg_shared_urls_flag = True
                                        for _url in outlets:
                                            if _url in msg_url1:
                                                msg_shared_urls_flag = False
                                                with open("./Output/Tabular/shared_urls.tsv", "a",
                                                          encoding="utf-8") as f:
                                                    f.write(
                                                        f"{msg_url1}\t{'msg'}\t{outlets[_url]}\t{group_name1}\t{group_id1}\t{creation_time1}\t{group_name2}\t{group_id2}\t{creation_time2}\n")
                                                break

                                        if msg_shared_urls_flag:
                                            with open("./Output/Tabular/shared_urls.tsv", "a", encoding="utf-8") as g:
                                                g.write(
                                                    f"{msg_url1}\t{'msg'}\t{outlets[_url]}\t{group_name1}\t{group_id1}\t{creation_time1}\t{group_name2}\t{group_id2}\t{creation_time2}\n")

                            for desc_url1 in desc_urls1:
                                for desc_url2 in desc_urls2:
                                    if desc_url1 == desc_url2:

                                        desc_shared_urls_flag = True

                                        if network.has_edge(group_name1, group_name2):
                                            network.edges[group_name1, group_name2]["total_weight"] += 1
                                            network.edges[group_name1, group_name2]["total_desc_weight"] += 1
                                            network.edges[group_name1, group_name2]["desc_url_weight"][desc_url1] = \
                                            network.edges[group_name1, group_name2]["desc_url_weight"].get(desc_url1,
                                                                                                           0) + 1
                                        else:
                                            network.add_edge(group_name1, group_name2,
                                                             total_weight=1,
                                                             total_msg_weight=0,
                                                             total_desc_weight=1,
                                                             msg_url_weight={},
                                                             desc_url_weight={desc_url1: 1},
                                                             fringe_url_weight={},
                                                             russian_url_weight={})

                                        for _url in outlets:
                                            if _url in desc_url1:
                                                network.edges[group_name1, group_name2][outlets[_url]] = network.edges[
                                                                                                             group_name1, group_name2].get(
                                                    outlets[_url], 0) + 1
                                                if outlets[_url] == "russian_outlet":
                                                    network.edges[group_name1, group_name2]["russian_url_weight"][
                                                        _url] = network.edges[group_name1, group_name2][
                                                                    "russian_url_weight"].get(_url, 0) + 1
                                                elif outlets[_url] == "fringe_community":
                                                    network.edges[group_name1, group_name2]["fringe_url_weight"][_url] = \
                                                    network.edges[group_name1, group_name2]["fringe_url_weight"].get(
                                                        _url, 0) + 1

                                                if fringe_russian_network.has_edge(group_name1, group_name2):
                                                    fringe_russian_network.edges[group_name1, group_name2][
                                                        "total_weight"] += 1
                                                    fringe_russian_network.edges[group_name1, group_name2][
                                                        "total_desc_weight"] += 1
                                                    fringe_russian_network.edges[group_name1, group_name2][
                                                        "desc_url_weight"][_url] = \
                                                    fringe_russian_network.edges[group_name1, group_name2][
                                                        "desc_url_weight"].get(_url, 0) + 1
                                                else:
                                                    fringe_russian_network.add_edge(group_name1, group_name2,
                                                                                    total_weight=1,
                                                                                    total_msg_weight=0,
                                                                                    total_desc_weight=1,
                                                                                    msg_url_weight={},
                                                                                    desc_url_weight={_url: 1})

                                                if outlets[_url] == "fringe_community":
                                                    if fringe_network.has_edge(group_name1, group_name2):
                                                        fringe_network.edges[group_name1, group_name2][
                                                            "total_weight"] += 1
                                                        fringe_network.edges[group_name1, group_name2][
                                                            "total_desc_weight"] += 1
                                                        fringe_network.edges[group_name1, group_name2][
                                                            "desc_url_weight"][_url] = \
                                                        fringe_network.edges[group_name1, group_name2][
                                                            "desc_url_weight"].get(_url, 0) + 1
                                                    else:
                                                        fringe_network.add_edge(group_name1, group_name2,
                                                                                total_weight=1,
                                                                                total_msg_weight=0,
                                                                                total_desc_weight=1,
                                                                                msg_url_weight={},
                                                                                desc_url_weight={_url: 1})
                                                elif outlets[_url] == "russian_outlet":
                                                    if russian_network.has_edge(group_name1, group_name2):
                                                        russian_network.edges[group_name1, group_name2][
                                                            "total_weight"] += 1
                                                        russian_network.edges[group_name1, group_name2][
                                                            "total_desc_weight"] += 1
                                                        russian_network.edges[group_name1, group_name2][
                                                            "desc_url_weight"][_url] = \
                                                        russian_network.edges[group_name1, group_name2][
                                                            "desc_url_weight"].get(_url, 0) + 1
                                                    else:
                                                        russian_network.add_edge(group_name1, group_name2,
                                                                                 total_weight=1,
                                                                                 total_msg_weight=0,
                                                                                 total_desc_weight=1,
                                                                                 msg_url_weight={},
                                                                                 desc_url_weight={_url: 1})

                                                desc_shared_urls_flag = False
                                                with open("./Output/Tabular/shared_urls.tsv", "a",
                                                          encoding="utf-8") as h:
                                                    h.write(
                                                        f"{desc_url1}\t{'desc'}\t{outlets[_url]}\t{group_name1}\t{group_id1}\t{creation_time1}\t{group_name2}\t{group_id2}\t{creation_time2}\n")
                                                break

                                        if desc_shared_urls_flag:
                                            with open("./Output/Tabular/shared_urls.tsv", "a", encoding="utf-8") as w:
                                                w.write(
                                                    f"{desc_url1}\t{'desc'}\t{'neither_fringe_nor_russian'}\t{group_name1}\t{group_id1}\t{creation_time1}\t{group_name2}\t{group_id2}\t{creation_time2}\n")


        return network, fringe_network, russian_network, fringe_russian_network
