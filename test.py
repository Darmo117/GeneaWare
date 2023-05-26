import owlready2 as o2

onto = o2.get_ontology('ontology.owl').load()
print(onto.base_iri)
with onto:
    # TODO define has_ascendant/has_descendant from has_parent/has_child
    p1 = onto.Person('P1')
    p2 = onto.Person('P2')
    p3 = onto.Person('P3')
    p1.was_main_actor_in.append(onto.Birth())
    p2.was_main_actor_in.append(onto.Birth())
    p3.was_main_actor_in.append(onto.Birth())
    # p2.has_parent.append(p1)
    # p1.was_main_actor_in.append(onto.Death())
    o2.close_world(onto)
    o2.sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    print(p1.has_descendant, p2.has_ascendant, p3.has_ascendant, p1.has_child, p2.has_parent, p3.has_parent)
    print(p1.is_a)
    print(p2.is_a)
    print(p1.was_main_actor_in, p2.was_main_actor_in, p3.was_main_actor_in)
