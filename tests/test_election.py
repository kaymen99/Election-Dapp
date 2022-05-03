import time, brownie
from brownie import Election
from scripts.helper_scripts import get_account


def test_deploy_election():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    assert election_contract.admin() == admin
    assert election_contract.electionCurrentState() == 0

def test_add_candidate():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    add_candidate_tx = election_contract.addCandidate("Candidate 1", {"from": admin})
    add_candidate_tx.wait(1)

    candidates_list = election_contract.getCandidatesList()
    candidate = candidates_list[0]

    assert len(candidates_list) == 1
    assert candidate[0] == 0
    assert candidate[1] == "Candidate 1"
    assert candidate[2] == 0

def test_open_election():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    add_candidate_tx = election_contract.addCandidate("Candidate 1", {"from": admin})
    add_candidate_tx.wait(1)

    # 1 day = 1 * 24 * 3600 s
    duration = 24 * 3600
    open_tx = election_contract.openVoting(duration, {"from": admin})
    open_tx.wait(1)

    start_time = open_tx.events["VoteOpened"]["timestamp"]

    vote_end_time = start_time + duration

    assert election_contract.electionCurrentState() == 1
    assert election_contract.voteEndTimestamp() == vote_end_time

def test_vote():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    add_candidate_tx = election_contract.addCandidate("Candidate 1", {"from": admin})
    add_candidate_tx.wait(1)

    # 1 day = 1 * 24 * 3600 s
    duration = 24 * 3600
    open_tx = election_contract.openVoting(duration, {"from": admin})
    open_tx.wait(1)

    user = get_account(1)

    candidate_id = 0

    vote_tx = election_contract.vote(candidate_id, {"from": user})
    vote_tx.wait(1)

    candidate_votes_count = election_contract.getVoteCount(candidate_id)

    user_vote = election_contract.getUserVote(user)

    assert candidate_votes_count == 1
    assert user_vote == candidate_id

def test_close_election():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    add_candidate_tx = election_contract.addCandidate("Candidate 1", {"from": admin})
    add_candidate_tx.wait(1)

    # duration = 10 s
    duration = 10
    open_tx = election_contract.openVoting(duration, {"from": admin})
    open_tx.wait(1)

    time.sleep(10)

    close_tx = election_contract.endVoting({"from": admin})
    close_tx.wait(1)

    assert election_contract.electionCurrentState() == 2

def test_close_election_before_deadline():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    add_candidate_tx = election_contract.addCandidate("Candidate 1", {"from": admin})
    add_candidate_tx.wait(1)

    # duration = 300 s
    duration = 300
    open_tx = election_contract.openVoting(duration, {"from": admin})
    open_tx.wait(1)

    # wait 20s
    time.sleep(20)
    
    # make sure that the contract throw an error when trying to close the election before deadline
    with brownie.reverts("Vote duration not ended"):
        close_tx = election_contract.endVoting({"from": admin})
        close_tx.wait(1)

def test_get_result():
    admin = get_account()
    election_contract = Election.deploy({"from": admin})

    add_candidate_tx = election_contract.addCandidate("Candidate 1", {"from": admin})
    add_candidate_tx.wait(1)

    add_candidate_tx = election_contract.addCandidate("Candidate 2", {"from": admin})
    add_candidate_tx.wait(1)

    # duration = 20 s
    duration = 20
    open_tx = election_contract.openVoting(duration, {"from": admin})
    open_tx.wait(1)

    user_1 = get_account(1)
    vote_tx = election_contract.vote(1, {"from": user_1})
    vote_tx.wait(1)

    user_2 = get_account(2)
    vote_tx = election_contract.vote(1, {"from": user_2})
    vote_tx.wait(1)

    time.sleep(20)

    close_tx = election_contract.endVoting({"from": admin})
    close_tx.wait(1)

    winner = election_contract.getResult()

    assert winner[0] == 1
    assert winner[1] == "Candidate 2"
    assert winner[2] == 2
