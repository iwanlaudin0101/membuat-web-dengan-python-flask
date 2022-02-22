from flask import request, make_response
from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa
from app import response, db

"""============API DOSEN============"""
def getDosen():
    try:
        datas = Dosen.query.all()
        data = []
        for i in datas:
            data.append(singleDosen(i))
        return response.success(data, 'Success')
    except Exception as e:
        print(e)

def singleDosen(data):
    data = {
        'id' : data.id,
        'nidn' : data.nidn,
        'name' : data.name,
        'phone' : data.phone,
        'addres' : data.addres
    }
    return data

def getDosenDetail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], 'Data tidak ditemukan!')

        mahasiswa = Mahasiswa.query.filter((Mahasiswa.dosen_satu==id) | (Mahasiswa.dosen_dua==id))
        datamahasiswa = []
        for mhs in mahasiswa:
            datamahasiswa.append(singleMahasiswa(mhs))

        data = singleDetailDosen(dosen, datamahasiswa)

        return response.success(data, 'Success')
    except Exception as e:
        print(e)

def singleDetailDosen(dosen, mahasiswa):
    data = {
        'id': dosen.id,
        'nidn': dosen.nidn,
        'name': dosen.name,
        'phone': dosen.phone,
        'mahasiswa': mahasiswa
    }
    return data

def singleMahasiswa(datas):
    data = {
        'id': datas.id,
        'nim': datas.nim,
        'name': datas.name,
        'phone': datas.phone
    }
    return data

def setDosen():
    try:
        nidn = request.form.get('nidn')
        name = request.form.get('name')
        phone= request.form.get('phone')
        addres= request.form.get('addres')

        data = Dosen(nidn=nidn, name=name, phone=phone, addres=addres)
        db.session.add(data)
        db.session.commit()

        return response.success('', 'Berhasil menambahkan data!')
    except Exception as e:
        print(e)
    
def update(id):
    try:
        nidn = request.form.get('nidn')
        name = request.form.get('name')
        phone= request.form.get('phone')
        addres= request.form.get('addres')
        
        data = {
            'nidn': nidn,
            'name': name,
            'phone': phone,
            'addres': addres
        }

        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], 'Data tidak ditemukan!')
        dosen.nidn = nidn
        dosen.name = name
        dosen.phone = phone
        dosen.addres = addres

        db.session.commit()
        return response.success(data, 'Success')
    except Exception as e:
        print(e)

def delete(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([], 'Data tidakditemukan')
        db.session.delete(dosen)
        db.session.commit()

        return response.success('', 'Success')
    except Exception as e:
        print(e)

"""============END API DOSEN============"""

"""============API MAHASISWA============"""
