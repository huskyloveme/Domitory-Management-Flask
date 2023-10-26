use domitory_management_1;
-- toa nha
insert into buildings(name, address) value('Tòa nhà KTX A','Km10, Đường Nguyễn Trãi, Q.Hà Đông, Hà Nội');

-- phong ktx
insert into rooms(name,accommodate,type,capacity,price,status,building_id) value ('101', 'Vệ sinh khép kín', 'PRIVATE',4,500000,'AVAILABLE', (select id from buildings where name like 'Tòa nhà KTX A'));
insert into rooms(name,accommodate,type,capacity,price,status,building_id) value ('102', 'Có sẵn nội thất', 'PUBLIC', 4, 350000,'AVAILABLE', (select id from buildings where name like 'Tòa nhà KTX A'));
insert into rooms(name,accommodate,type,capacity,price,status,building_id) value ('103', 'Có sẵn nội thất', 'PUBLIC', 4, 350000,'UNAVAILABLE', (select id from buildings where name like 'Tòa nhà KTX A'));
insert into rooms(name,accommodate,type,capacity,price,status,building_id) value ('104', 'Vệ sinh khép kín', 'PUBLIC', 4, 500000,'UNAVAILABLE', (select id from buildings where name like 'Tòa nhà KTX A'));
insert into rooms(name,accommodate,type,capacity,price,status,building_id) value ('105', 'Vệ sinh khép kín', 'PUBLIC', 4, 500000,'AVAILABLE', (select id from buildings where name like 'Tòa nhà KTX A'));

-- sinh vien
insert into students(room_id, msv, name, address, phone, gender, birthday, day_in, day_out, status) value ((select id from rooms where name like '101'), 'B18DCVT229', 'Nguyen Van A', 'Hoai Duc, Ha Noi' , '09842596511', 'MALE', '2000-01-01 00:00:00', '2018-07-01 00:00:00', '2018-12-31 23:59:59', 'ACTIVE');
insert into students(room_id, msv, name, address, phone, gender, birthday, day_in, day_out, status) value ((select id from rooms where name like '101'), 'B18DCVT239', 'Nguyen Van B', 'Tran Phu, Ha Dong, Ha Noi' , '09842596521', 'FEMALE', '2000-01-01 00:00:00', '2018-07-01 00:00:00', '2018-12-31 23:59:59', 'ACTIVE');

-- khach den tham sinh vien
insert into vistors(student_id, cccd, name, phone, gender, time_in, time_out) value ( (select id from students where msv like 'B18DCVT239'), '001082946357', 'Tran Van Nam', '0983867797', 'MALE', now(), date_add(now(),interval 2 hour));

-- dich vu
insert into services(name, price, unit, description) value ('Trông xe', 100000, 'tháng', 'Mỗi xe được gửi 2 lần miễn phí trong ngày');
insert into services(name, price, unit, description) value ('Ăn uống', '35000', 'suất', 'Mỗi suất có giá trị trong một ngày');
insert into services(name, price, unit, description) value ('Giặt là', '50000', 'kg', 'Mỗi phiếu có giá trị 1 lần sử dụng trong ngày');

-- sinh vien su dung dich vu
insert into student_service(student_id, service_id, time_use, time_end) value ( (select id from students where msv like 'B18DCVT229'), (select id from services where name like 'Trông xe'), 1, date_add(now(), INTERVAL 1 month ) );
insert into student_service(student_id, service_id, time_use, time_end) value ( (select id from students where msv like 'B18DCVT239'), (select id from services where name like 'Ăn uống'), 1,  date_add(CURDATE(), interval 24*60*60 - 1 second));

-- xe may dang ky cua sinh vien
insert into motorbikes(student_id, name, license_plate, time_registration, status) value ( (select id from students where msv like 'B18DCVT229'), 'Honda Vision 2021', '29X1 77821', now(), 'REGISTER');
insert into motorbikes(student_id, name, license_plate, time_registration, status) value ( (select id from students where msv like 'B18DCVT229'), 'Honda Wave 2021', '29X1 14245', now(), 'REGISTER');

-- lich su gui xe
insert into parking_histories(motorbike_id, time_in, time_out, status, price) value ((select id from motorbikes where license_plate like '29X1 77821'), now(), date_add(now(),interval 2 hour), 'FREE',0);