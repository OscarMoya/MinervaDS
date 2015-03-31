
class MatchManager:

    def __init__(self):
        self.matches = dict()

    def check_in(self, match):
        root = match.get_root()

        if root in self.matches.keys():
            if not match in self.matches.get(root):
                self.matches[root].append(match)
        else:
            self.matches[root] = [match]

    def take_off(self):
        result = list()
        departed_roots = list()
        for root in self.matches:
            if len(self.matches.get(root)) == 3:
                result.append(self.matches[root])
                departed_roots.append(root)
        for root in departed_roots:
            self.matches.pop(root)
        return result


class Match:

    def __init__(self, match_type="client"):
        self.in_port = None
        self.src_mac = None
        self.dst_mac = None
        self.eth_type = None
        self.vlan_id = None
        self.vlan_priority = None
        self.src_ip = None
        self.dst_ip = None
        self.ip_tos = None
        self.l3_src_port = None
        self.l3_dst_port = None
        self.match_type = match_type
        
        if match_type == "client":
            self.__root_headers = {"in_port": self.get_in_port, "src_mac": self.get_src_mac, "eth_type": self.get_eth_type, "vlan_id": self.get_vlan_id, "src_ip": self.get_src_ip}
        else:
            self.__root_headers = {"eth_type": self.get_eth_type, "vlan_id": self.get_vlan_id, "src_ip": self.get_src_ip}

    def get_root(self):
        #print "match_type", self.match_type
        root = Match(self.match_type)
        for attr in self.__root_headers:
            setattr(root, attr, self.__root_headers[attr]())
        return root

    def get_in_port(self):
        return self.in_port

    def get_src_mac(self):
        return self.src_mac

    def get_dst_mac(self):
        return self.dst_mac

    def get_eth_type(self):
        return self.eth_type

    def get_vlan_id(self):
        return self.vlan_id

    def get_vlan_prority(self):
        return self.vlan_priority

    def get_src_ip(self):
        return self.src_ip

    def get_dst_ip(self):
        return self.dst_ip

    def get_ip_tos(self):
        return self.ip_tos

    def get_l3_src_port(self):
        return self.l3_src_port

    def get_l3_dst_port(self):
        return self.get_l3_dst_port()

    def __hash__(self):
        result = 31 * 1
        attrs = self.__dict__
        for attr in attrs:
            if attr == "_Match__root_headers":
                continue
            if attrs[attr]:
                result += 31 * hash(attrs[attr])
        return result

    def __eq__(self, other):
        attrs = self.__dict__.keys()
        result = True
        for attr in attrs:
            if attr == "_Match__root_headers":
                continue
            if not getattr(self, attr) == getattr(other, attr):
                result = False
        return result


if __name__ == "__main__":

    match1 = Match()
    match2 = Match()
    match3 = Match()
    i = 0
    for attr in match1.__dict__:
        if "__" not in attr:
            setattr(match1, attr, i)
            setattr(match2, attr, i)
            setattr(match3, attr, i)
            i += 1

    match2.dst_ip = 44
    match3.dst_ip = 54

    manager = MatchManager()
    manager.check_in(match1)
    manager.check_in(match2)
    manager.check_in(match3)

    result = manager.take_off()
    for list in result:
        for match in list:
            root_dict = match.in_port
