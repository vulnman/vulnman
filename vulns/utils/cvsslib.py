import cvss


def get_scores_by_vector(vector):
    return cvss.CVSS3(vector).scores()
