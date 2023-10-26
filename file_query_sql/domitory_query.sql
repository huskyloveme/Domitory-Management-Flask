use domitory_management;

-- In thông tin sinh viên trong ký túc xá 
-- cùng với số tiền mà họ phải trả cho tất cả các dịch vụ (bao gồm tiền phòng) 
-- đã sử dụng trong mỗi tháng
create or replace view domitory_management.rooms_statics as -- tao ra bang view ao de query
select students.id, students.msv, students.name, students.address, students.phone, 
	students.day_in, students.day_out, rooms.name as room_name, rooms.price as room_price,
	(services.price * sum(student_service.time_use)) as service_price -- tong gia tien moi dich vu	
	from students inner join rooms on rooms.id = students.room_id
    inner join student_service on student_service.student_id = students.id
    inner join services on student_service.service_id = services.id
    where student_service.created_at between date_add(date_add(LAST_DAY(now()),interval 1 DAY),interval -1 MONTH) 
    and LAST_DAY(curdate())
    group by student_service.service_id, student_service.student_id;

select id, name, address, phone, -- query bang view de tinh tong
	day_in, day_out, room_name, room_price, 
    sum(service_price) as total_service_price,
    (sum(service_price) + room_price) as total_price
    from domitory_management.rooms_statics 
    group by msv;

-- In thông tin sinh viên cùng với tên dịch 
-- tổng giá mỗi dịch vụ mà họ sử dụng trong khoảng thời gian 
-- từ ngày bắt đầu đến ngày kết thúc
select student_service.student_id,
	students.name, students.msv,
	student_service.service_id,
    services.name, services.price,
    sum(student_service.time_use) as time_use, -- tong so lan su dung moi dich vu
    (services.price * sum(student_service.time_use)) as total_price -- tong gia tien cho moi dich vu
	from student_service 
    inner join services on student_service.service_id = services.id
    inner join students on student_service.student_id = students.id
	where student_service.created_at between date_add(date_add(LAST_DAY(now()),interval 1 DAY),interval -1 MONTH) 
    and LAST_DAY(curdate()) -- query tu ngay bat dau cua thang den ngay ket thuc cua thang
    group by service_id, student_id;
    
-- In danh mục các dịch vụ cùng doanh thu của mỗi dịch vụ trong KTX mỗi tháng
select services.name, services.price,
	sum(student_service.time_use) as time_use,
    (services.price * sum(student_service.time_use)) as total_price
	from services
	inner join student_service on student_service.service_id = services.id
    where student_service.created_at between date_add(date_add(LAST_DAY(now()),interval 1 DAY),interval -1 MONTH) 
    and LAST_DAY(curdate())
	group by service_id;
    
-- In thông tin sinh viên cùng thông tin về các khách đến thăm họ trong tuần, hoặc tháng
-- cùng số lần mỗi khách đến thăm