# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: An Early Romana
- Step 0.12, results of the three runs without a session (optional): Run 1: 401 FAILED, Run 2: 200 PASSED, Run 3: 401 FAILED (Flaky test due to lack of session cookie across load balancer)
- Step 0.16, blocks of "how many of the three tools are excluded":
  - Block 0 (0 tools excluded): `[]`
  - Block 1 (1 tool excluded): `["Knife"]`, `["Scissors"]`, `["Pizza cutter"]`
  - Block 2 (2 tools excluded): `["Knife", "Scissors"]`, `["Knife", "Pizza cutter"]`, `["Pizza cutter", "Scissors"]`
  - Block 3 (3 tools excluded / all tools excluded): `["Knife", "Pizza cutter", "Scissors"]`

## Defect report
- Title: Server returns 500 Internal Server Error with empty body when all available tools are excluded
- Request: `POST /api/pizza` with header `Authorization: token <token>` and body `{"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}`
- Expected result: HTTP 400 Bad Request with a clear JSON error message explaining that no pizza satisfies the restriction (e.g. `{"error": "no pizza satisfies the excluded tools"}`)
- Actual result: HTTP 500 Internal Server Error with an empty response body (`Content-Length: 0`)
- Severity: Medium to High (Unhandled server exception crashing the request handling instead of gracefully rejecting invalid customer restrictions)

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - Read (GET `/api/ratings/{id}`): 404 Not Found
  - Change (PUT `/api/ratings/{id}`): 400 Bad Request
  - Delete (DELETE `/api/ratings/{id}`): 400 Bad Request

## Part B
1. **Two kinds of failure real server tests find that stubs cannot, and one reason to write unit tests with stubs:**
   - Real server tests find:
     1. Integration and deployment issues, such as HTTP headers, session routing, load balancer sticky session cookies (`AWSALB`), and network latency/timeouts.
     2. Database and backend constraint violations, data serialization/deserialization mismatches (such as Go struct parsing errors), and real concurrency conflicts.
   - Reason to write unit tests with stubs:
     - They execute in milliseconds in complete isolation without external dependencies or network unreliability, allowing developers to isolate and debug algorithm logic defects quickly and precisely.

2. **Why every test creates its own user with a new name, rather than use the public token, and how to apply in Project 2:**
   - QuickPizza is a shared environment used concurrently by multiple testers. If all tests shared the public token, one test could mutate, overwrite, or delete ratings while another test is reading them, leading to race conditions and test interference.
   - For Project 2 (shared shop or hotel API), each test must provision its own isolated entity (e.g. unique user, cart, or reservation identifier) or separate clean state, ensuring tests remain strictly independent.

3. **Why the tests send every request through one session, and description of Step 0.12:**
   - QuickPizza runs behind an AWS Application Load Balancer with multiple backend server nodes. The load balancer sets an `AWSALB` cookie to route requests from the same client to the same backend server (sticky session). A `requests.Session` automatically persists and sends this cookie across all requests.
   - In Step 0.12 without a session, requests did not preserve cookies. In three runs, Run 1 and Run 3 failed with `401 Unauthorized` at login (because the login request hit a different server that did not know the newly registered user), while Run 2 passed. This produced a flaky test.

4. **Which block of excluded tools revealed the defect in Step 0.16, why 500 is worse than 400, and why use xfail instead of deleting:**
   - Block 3 (all 3 tools excluded: `["Knife", "Pizza cutter", "Scissors"]`) triggered the defect.
   - An HTTP 500 with an empty body represents an unhandled server-side crash that leaves the client application blind to what went wrong. In contrast, an HTTP 400 with a descriptive JSON message clearly communicates client-side error conditions so the client can display meaningful user feedback.
   - Marking the test with `@pytest.mark.xfail(strict=True)` keeps the known bug documented in the test suite without failing the entire build pipeline, while `strict=True` ensures the suite flags an error as soon as the backend bug is fixed, prompting the team to update the test.

5. **Base choice coverage count vs all combinations coverage count for Step A1:**
   - Characteristics and blocks:
     - C1 (Value of stars): 3 blocks
     - C2 (Type of stars): 4 blocks
     - C3 (Pizza existence): 2 blocks
     - C4 (Token validity): 3 blocks
   - Base Choice Coverage (BCC):
     $1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 1 + 2 + 3 + 1 + 2 = 9$ tests.
   - All Combinations Coverage (ACC):
     $3 \times 4 \times 2 \times 3 = 72$ tests.

6. **Status codes in Step A4 and defect evaluation:**
   - Actual status codes obtained: GET returned `404 Not Found`, PUT returned `400 Bad Request`, DELETE returned `400 Bad Request`.
   - Expected status codes: Ideally `403 Forbidden` because the resource exists but belongs to a different user, or `404 Not Found` if the API deliberately conceals resource existence for privacy.
   - The status code `400 Bad Request` returned for PUT and DELETE is semantically inappropriate because 400 indicates a client syntax/payload error, whereas the payload is well-formed; the issue is authorization or resource visibility. This inconsistency represents an API design defect.

7. **Result of made-up token `0000000000000000` from `madeup.txt` and security risks:**
   - Running `curl -H "@madeup.txt" https://quickpizza.grafana.com/api/ratings` returns HTTP `200 OK` along with a list of 50 ratings from the system.
   - This is a serious defect (Broken Authentication / Improper Access Control). The server accepts arbitrary 16-character tokens without verifying that they belong to an active, valid authenticated session. On a real system, an attacker could forge tokens to access and harvest unauthorized data.

8. **One thing an API test checks better than a web page test, and one thing only a web page test can check:**
   - API tests check better: Backend business logic, response status codes, header details, and invalid/extreme input boundaries that might otherwise be blocked by client-side browser form validation.
   - Only web page tests can check: Real browser layout, visual appearance, CSS styling, responsiveness, element positioning, and actual human user experience / accessibility.
