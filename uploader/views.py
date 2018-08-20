from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import paramiko

# from .forms import UploadForm

class UploaderView(View):
	_hostname			= '13.228.81.171'
	_port				= 22311
	_username			= 'ubuntu'
	_password			= ''
	_rsa_private_key	= paramiko.RSAKey.from_private_key_file('/Users/ricky.fredy/.ssh/id_rsa')
	_folder_path		= '/home/ubuntu/lel/'
	_ssh				= paramiko.SSHClient()
	_isSuccessConnect	= False

	def __init__(self):
		self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	def get(self, request):
		try:
			# Connect to server via ssh
			self._ssh.connect(self._hostname, port=self._port, username=self._username, pkey = self._rsa_private_key)

			# Set success connect flag = True
			self._isSuccessConnect = True

			# Get SFTPClient
			self._sftp = self._ssh.open_sftp()

			# Change current directory
			self._sftp.chdir(self._folder_path)

			# Get file lsit
			file_list = self._sftp.listdir()

			self._ssh.close()
		except paramiko.SSHException as e:
			# Set success connect flag = False
			self._isSuccessConnect = False
			quit()
		
		# form = UploadForm()
		return render(request, 'uploader/index.html', {'isSuccessConnect': self._isSuccessConnect, 'file_list': file_list})


	def post(self, request):
		try:
			# Get all post data
			order_file = request.FILES['order_file']
			order_file.open()

			# file_name = request.POST['file_name']

			if order_file == False:
				return HttpResponse('No File Upload')
			# elif file_name == '':
			# 	return HttpResponse('No File Name')

			# Connect to server via ssh
			self._ssh.connect(self._hostname, port=self._port, username=self._username, pkey = self._rsa_private_key)

			# Set success connect flag = True
			self._isSuccessConnect = True

			# Get SFTPClient
			self._sftp = self._ssh.open_sftp()

			# Change current directory
			self._sftp.chdir(self._folder_path)

			# Copy file
			self._sftp.putfo(order_file, self._folder_path + 'new.csv')

			# Get file lsit
			file_list = self._sftp.listdir()

			self._ssh.close()
		except paramiko.SSHException:
			# Set success connect flag = False
			self._isSuccessConnect = False

		# form = UploadForm()
		return render(request, 'uploader/index.html', {'isSuccessConnect': self._isSuccessConnect, 'file_list': file_list})