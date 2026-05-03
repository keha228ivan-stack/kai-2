# Client -> Local Backend Integration

Backend base URL for all clients:
- `http://127.0.0.1:8000`

## Web (`hrrepozik`, manager role)
Use:
- `POST /auth/login`
- `POST /manager/assign`
- `GET /manager/employee_courses/{user_id}`
- `GET /library/sync`

## Mobile (`hrrepozik-modile-2`, admin role)
Use only:
- `GET /admin/stats`
- `GET /admin/stats/{department}`

Do not call employee/manager endpoints and do not show per-user details.

## Desktop (`repozik-desktop2`, employee role)
Use:
- `POST /auth/register`
- `POST /auth/login`
- `GET /employee/my_courses`
- `GET /employee/my_courses/{course_id}`
- `GET /employee/my_courses/{course_id}/progress`
- `PATCH /employee/my_courses/{course_id}/progress`
- `GET /employee/my_courses/{course_id}/test`
- `GET /library/sync`
