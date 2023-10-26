use domitory_management_1;
show triggers;

-- trigger khong cho dang ky qua so nguoi trong mot phong
delimiter $$
drop trigger if exists domitory_management_1.before_insert_students;
create trigger before_insert_students before insert on students
for each row
begin
	declare total integer;
    select count(*) into total from students s where s.room_id=new.room_id;
    if(total >= (select capacity from rooms where rooms.id = new.room_id) ) then
		signal sqlstate '45000' set MESSAGE_TEXT = 'Room is full' ;
	end if;
end $$
delimiter ;

-- trigger khong cho dang ky qua so nguoi trong mot phong
delimiter $$
drop trigger if exists domitory_management_1.before_update_students;
create trigger before_update_students before update on students
for each row
begin
	declare total integer;
    select count(*) into total from students s where s.room_id=new.room_id;
    if(total >= (select capacity from rooms where rooms.id = new.room_id) ) then
		signal sqlstate '45000' set MESSAGE_TEXT = 'Room is full' ;
	end if;
end $$
delimiter ;
-- trigger khong cho dang ky qua 2 xe
delimiter $$
drop trigger if exists domitory_management_1.before_insert_motorbikes;
create trigger before_insert_motorbikes before insert on motorbikes
for each row
begin
	declare total integer;
	select count(*) into total from motorbikes m where m.student_id=new.student_id and m.status = 'REGISTER';
    if(total >= 2 ) then
		signal sqlstate '45000' set MESSAGE_TEXT = 'Maxiumum number of motorbike registrations' ;
	end if;
end $$
delimiter ;

-- trigger check 2 lan gui xe mien phi trong 1 ngay
delimiter $$
drop trigger if exists domitory_management_1.before_insert_parking_histories;
create trigger before_insert_parking_histories before insert on parking_histories
for each row
begin
	declare total integer;
	select count(*) into total from parking_histories pk
		where pk.status = 'FREE'
        and pk.motorbike_id=new.motorbike_id and time_in >= curdate();
	if(total <=> 2) then
		set new.status = 'PAID';
        set new.price = 3000;
    end if;
end $$
delimiter ;